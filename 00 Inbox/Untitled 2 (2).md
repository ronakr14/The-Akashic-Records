# SSL Certificate Verification Issue – Investigation & Handoff Document

## Problem Summary

Application logs are reporting SSL certificate verification failures:

```text
2026-06-11T06:09:02.749Z [Rudder] error: Response error code: UNABLE_TO_GET_ISSUER_CERT_LOCALLY
2026-06-11T06:09:02.809Z [Rudder] error: Error: UNABLE_TO_GET_ISSUER_CERT_LOCALLY
unable to get local issuer certificate
unable to get local issuer certificate
```

The error indicates that the client cannot validate the certificate chain presented by the remote HTTPS endpoint.

---

## Current Assessment

Most likely root cause:

### 1. Corporate SSL Inspection Proxy (High Probability)

Traffic is routed through a corporate security appliance such as:

- Zscaler
    
- Netskope
    
- BlueCoat
    
- Fortinet
    
- Palo Alto
    
- Similar SSL interception solutions
    

Architecture:

```text
Application
    ↓
Corporate SSL Proxy
    ↓
External Service
```

The proxy generates its own certificates, but the local Python environment does not trust the proxy's root Certificate Authority (CA).

Estimated likelihood: ~80%

---

### 2. Missing Corporate Root CA in Python Trust Store

Windows may trust the certificate while Python's bundled certificate store (certifi) does not.

Estimated likelihood: ~15%

---

### 3. Remote Service Certificate Chain Problem

The external service may be serving an incomplete certificate chain.

Estimated likelihood: ~5%

---

## Systems Potentially Impacted

Observed in:

- RudderStack SDK / Agent
    

Potentially impacted:

- OpenRouter API
    
- OpenAI API
    
- Anthropic API
    
- Internal HTTPS integrations
    
- Python requests
    
- Python httpx
    
- Node.js HTTPS clients
    

---

## Diagnostic Steps

### Verify Python SSL Configuration

```python
import ssl

print(ssl.get_default_verify_paths())
```

Expected outcome:

- Determine certificate bundle currently being used.
    

---

### Verify Certifi Installation

```bash
pip show certifi
```

Expected outcome:

- Identify certificate bundle path.
    
- Confirm certifi installation status.
    

---

### Test External HTTPS Connectivity

```python
import requests

requests.get("https://openrouter.ai")
```

Expected outcome:

- Success → issue isolated elsewhere.
    
- SSL failure → certificate trust issue confirmed.
    

---

### Inspect Presented Certificate

Browser Steps:

1. Open target website
    
2. Click Lock Icon
    
3. View Certificate
    
4. View Certification Path
    

Check for issuers such as:

- Zscaler
    
- Netskope
    
- BlueCoat
    
- Fortinet
    
- Palo Alto
    

Presence indicates SSL interception.

---

### OpenSSL Validation

```bash
openssl s_client -connect openrouter.ai:443 -showcerts
```

Expected outcome:

- Full certificate chain displayed.
    
- Ability to identify missing issuer certificates.
    

---

## Remediation Options

### Option A: Install Corporate Root Certificate (Recommended)

Obtain root CA certificate from IT/Security team.

Configure Python:

```python
import httpx

client = httpx.Client(
    verify=r"C:\certs\company-root.pem"
)
```

or

```bash
set SSL_CERT_FILE=C:\certs\company-root.pem
```

---

### Option B: Extend Certifi Bundle

Locate certifi bundle:

```python
import certifi
print(certifi.where())
```

Create combined bundle:

```text
certifi.pem
+ company-root.pem
-------------------
combined.pem
```

Use:

```python
client = httpx.Client(
    verify="combined.pem"
)
```

---

### Option C: Trust Windows Certificate Store

Install:

```bash
pip install python-certifi-win32
```

This synchronizes Python certificate trust with Windows trusted roots.

---

### Option D: Environment Variables

```bash
set SSL_CERT_FILE=C:\certs\company-root.pem
set REQUESTS_CA_BUNDLE=C:\certs\company-root.pem
```

PowerShell:

```powershell
$env:SSL_CERT_FILE="C:\certs\company-root.pem"
$env:REQUESTS_CA_BUNDLE="C:\certs\company-root.pem"
```

---

### Option E: Disable Verification (Diagnostic Only)

Not suitable for production.

```python
requests.get(url, verify=False)
```

or

```python
client = httpx.Client(verify=False)
```

If this succeeds, SSL trust configuration is confirmed as the root cause.

---

## Recommended Next Actions

### Immediate

- Run SSL verification diagnostics.
    
- Capture Python trust store configuration.
    
- Capture certifi version.
    
- Inspect certificate chain from browser.
    

### Short Term

- Obtain corporate root CA certificate.
    
- Configure Python trust store.
    

### Long Term

- Standardize certificate management across:
    
    - Python
        
    - Node.js
        
    - CI/CD agents
        
    - Developer workstations
        
- Document corporate CA installation process.
    

---

## Information Needed From Environment

Please collect:

### Python SSL Paths

```python
import ssl
print(ssl.get_default_verify_paths())
```

### Certifi Details

```bash
pip show certifi
```

### OpenSSL Output

```bash
openssl s_client -connect openrouter.ai:443 -showcerts
```

### Browser Certificate Path Screenshot

Capture certification path showing issuer chain.

---

## Expected Resolution

After importing the corporate root CA into the trust store used by Python, HTTPS requests should successfully validate certificates and the following error should disappear:

```text
UNABLE_TO_GET_ISSUER_CERT_LOCALLY
unable to get local issuer certificate
```