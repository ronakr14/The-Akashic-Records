# n8n Startup SSL Error Investigation – Handoff Document

## Problem Statement

During n8n startup, the following errors are observed:

```text
2026-06-11T06:09:02.749Z [Rudder] error: Response error code: UNABLE_TO_GET_ISSUER_CERT_LOCALLY
2026-06-11T06:09:02.809Z [Rudder] error: Error: UNABLE_TO_GET_ISSUER_CERT_LOCALLY
unable to get local issuer certificate
unable to get local issuer certificate
```

Initial assumption was an SSL certificate trust issue affecting outbound HTTPS communication from n8n.

---

# Environment Information

## Platform

- Windows
    
- PowerShell
    
- n8n
    
- RudderStack telemetry integration emitting errors
    

---

# Investigation Performed

## Check 1: Environment Variables

Command:

```powershell
Get-ChildItem Env: | Where-Object {
    $_.Name -match "PROXY|SSL|CERT"
}
```

Result:

```text
No output
```

Conclusion:

- No custom SSL certificate configuration
    
- No proxy environment variables configured
    

---

## Check 2: WinHTTP Proxy

Command:

```powershell
netsh winhttp show proxy
```

Result:

```text
Current WinHTTP proxy settings:

    Direct access (no proxy server).
```

Conclusion:

- No system-level WinHTTP proxy configured
    

---

## Check 3: RudderStack Endpoint Connectivity

Command:

```powershell
Invoke-WebRequest https://api.rudderstack.com
```

Result:

```text
Invoke-WebRequest : Not Found
```

HTTP response successfully returned.

Conclusion:

- DNS resolution works
    
- Network connectivity works
    
- TLS handshake succeeds
    
- Windows trust store accepts server certificate
    

This significantly reduces the likelihood of a machine-wide SSL issue.

---

# Updated Root Cause Hypothesis

Since PowerShell successfully establishes TLS connections:

```text
Windows Trust Store = Healthy
Network Connectivity = Healthy
DNS Resolution = Healthy
```

The issue likely exists within:

1. n8n bundled Node.js runtime
    
2. Embedded certificate bundle
    
3. Corporate SSL inspection certificate not trusted by Node
    
4. RudderStack telemetry client configuration
    

---

# Most Likely Scenarios

## Scenario A (Most Likely)

Corporate SSL interception exists.

Examples:

- Zscaler
    
- Netskope
    
- Bluecoat
    
- Palo Alto SSL inspection
    

Windows trusts the corporate CA, but Node.js inside n8n does not.

Symptoms:

```text
PowerShell HTTPS works
Node.js HTTPS fails
n8n telemetry fails
```

---

## Scenario B

Node certificate store mismatch.

Node runtime uses a certificate bundle that does not contain the required root/intermediate CA.

---

## Scenario C

Telemetry-only issue.

RudderStack diagnostics fail but workflows continue functioning normally.

---

# Recommended Next Diagnostic Steps

## Verify Node Runtime

```powershell
node -v
```

Capture version.

---

## Verify Node HTTPS

```powershell
node -e "fetch('https://api.rudderstack.com').then(r=>console.log(r.status)).catch(e=>console.error(e))"
```

Expected outcomes:

### Success

```text
404
```

Meaning:

- Node SSL works
    

### Failure

```text
UNABLE_TO_GET_ISSUER_CERT_LOCALLY
```

Meaning:

- Node certificate trust issue confirmed
    

---

## Inspect Presented Certificate

```powershell
$tcp = New-Object System.Net.Sockets.TcpClient("api.rudderstack.com",443)
$ssl = New-Object System.Net.Security.SslStream($tcp.GetStream(),$false,({$true}))
$ssl.AuthenticateAsClient("api.rudderstack.com")

$cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($ssl.RemoteCertificate)

$cert.Issuer
```

Capture issuer.

Examples:

```text
CN=DigiCert ...
```

Normal.

or

```text
CN=Zscaler Root CA
```

Corporate interception confirmed.

---

# Temporary Mitigation

For testing only:

```powershell
$env:NODE_TLS_REJECT_UNAUTHORIZED="0"
n8n start
```

If error disappears:

- SSL trust issue confirmed
    

Do not use permanently.

---

# Permanent Remediation

## Export Corporate Root Certificate

Open:

```text
certlm.msc
```

Navigate:

```text
Trusted Root Certification Authorities
```

Export root certificate as:

```text
Base-64 encoded X.509 (.CER)
```

Example:

```text
C:\certs\corp-root.cer
```

---

## Configure Node

Temporary:

```powershell
$env:NODE_EXTRA_CA_CERTS="C:\certs\corp-root.cer"
n8n start
```

Permanent:

```powershell
[Environment]::SetEnvironmentVariable(
  "NODE_EXTRA_CA_CERTS",
  "C:\certs\corp-root.cer",
  "User"
)
```

Restart terminal/session.

---

# Telemetry Workaround

If workflows are unaffected and only diagnostics fail:

```powershell
$env:N8N_DIAGNOSTICS_ENABLED="false"
$env:N8N_PERSONALIZATION_ENABLED="false"

n8n start
```

This disables telemetry-related communication.

---

# Current Status

## Confirmed

- Windows networking operational
    
- TLS connectivity operational from PowerShell
    
- RudderStack endpoint reachable
    
- No system proxy configured
    
- No SSL-related environment overrides configured
    

## Not Yet Confirmed

- Node.js certificate trust behavior
    
- Corporate SSL inspection presence
    
- n8n runtime certificate chain
    
- Whether issue is telemetry-only
    

---

# Required Follow-Up Data

Please collect:

```powershell
node -v
```

```powershell
node -e "fetch('https://api.rudderstack.com').then(r=>console.log(r.status)).catch(e=>console.error(e))"
```

```powershell
$cert.Issuer
```

These three outputs should be sufficient to identify the final root cause.