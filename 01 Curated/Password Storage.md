---
domain: Security
domain_suggested: null
category: Curated
category_suggested: null
source_type: obsidian
status: review
tags: [password, security, authentication, hashing, argon2]
---






```table-of-contents
```

For modern password storage, the recommended approach is:

```
Password
   ↓
Pepper (secret from environment/HSM)
   ↓
Password Hashing Algorithm (Argon2id preferred)
   ↓
Store hash + salt in database
```

### Components

#### 1. Salt

- Unique random value per password.
    
- Prevents rainbow table attacks.
    
- Stored alongside the hash.
    
- Generated automatically by most libraries.
    

#### 2. Pepper

- Application-wide secret.
    
- Stored outside the database (environment variable, secret manager, HSM).
    
- If database is compromised, attacker still needs the pepper.
    
- Never store pepper in the same database as password hashes.
    

Example:

```python
pepper = os.environ["PASSWORD_PEPPER"]
password_to_hash = password + pepper
```

---

## Recommended Algorithms

### Argon2id (Current Best Practice)

Advantages:

- Memory hard
    
- Resistant to GPU cracking
    
- Recommended by OWASP and modern security guidance
    

Python library:

```bash
pip install argon2-cffi
```

Example:

```python
from argon2 import PasswordHasher
import os

ph = PasswordHasher()

pepper = os.environ["PASSWORD_PEPPER"]

password = "MyPassword123!"
hash_value = ph.hash(password + pepper)

print(hash_value)
```

Verify:

```python
try:
    ph.verify(hash_value, password + pepper)
    print("Valid")
except:
    print("Invalid")
```

---

### bcrypt

Still widely used but older than Argon2.

Library:

```bash
pip install bcrypt
```

Example:

```python
import bcrypt
import os

pepper = os.environ["PASSWORD_PEPPER"]

password = "MyPassword123!"
combined = (password + pepper).encode()

hashed = bcrypt.hashpw(
    combined,
    bcrypt.gensalt(rounds=12)
)

print(hashed.decode())
```

Verify:

```python
bcrypt.checkpw(
    (password + pepper).encode(),
    hashed
)
```

---

### scrypt

Built into Python standard library.

```python
import hashlib
import secrets

salt = secrets.token_bytes(16)

hash_value = hashlib.scrypt(
    b"password",
    salt=salt,
    n=16384,
    r=8,
    p=1
)
```

Good option if you want no external dependencies.

---

## Best Library Overall: Passlib

If you're building an application, use:

```bash
pip install passlib[argon2]
```

Passlib provides:

- Argon2
    
- bcrypt
    
- scrypt
    
- automatic hash migration
    
- algorithm identification
    

Example:

```python
from passlib.context import CryptContext
import os

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

pepper = os.environ["PASSWORD_PEPPER"]

hashed = pwd_context.hash(password + pepper)

pwd_context.verify(
    password + pepper,
    hashed
)
```

---

## Production Pattern

Store:

```sql
users
------
id
email
password_hash
```

Environment:

```bash
PASSWORD_PEPPER=super-secret-random-value
```

Hashing:

```python
hash = Argon2id(password + pepper)
```

Database stores:

```text
$argon2id$v=19$m=65536,t=3,p=4$...
```

The hash already contains:

- salt
    
- algorithm
    
- work factors
    

Only the pepper remains external.

### Current recommendation

For a new Python application:

- Algorithm: **Argon2id**
    
- Library: **`argon2-cffi`** or **`passlib[argon2]`**
    
- Use a **pepper** stored in a secret manager or environment variable
    
- Let the library manage salts automatically
    
- Never use plain SHA256, SHA512, or MD5 for password storage.

---

# Algorithm Comparison

| Algorithm | Memory Hard | GPU Resistant | Python Library | OWASP Recommendation | Status |
|---|---|---|---|---|---|
| **Argon2id** | Yes | Yes | `argon2-cffi` | 1st choice | Current best |
| **bcrypt** | No | Partial | `bcrypt` | Acceptable | Legacy safe |
| **scrypt** | Yes | Partial | `hashlib` (stdlib) | Acceptable | No deps needed |
| **PBKDF2-SHA256** | No | No | `hashlib` (stdlib) | Acceptable | FIPS compliant |
| **SHA-256 + salt** | No | No | `hashlib` | **Never** | Broken pattern |
| **MD5** | No | No | `hashlib` | **Never** | Broken since 2004 |

Key distinction: SHA-256 is a **fast hash**, not a **password hash**. Attackers can compute billions of SHA-256 hashes per second on a GPU. Argon2 is deliberately **slow and memory-hard**.

---

# Common Mistakes

### 1. Using SHA-256 with salt and calling it "secure"

```python
# WRONG — fast hash, easily brute-forced
hashlib.sha256(password + salt).hexdigest()

# CORRECT — slow, memory-hard KDF
argon2.PasswordHasher().hash(password + pepper)
```

### 2. Storing pepper in the database

Pepper must live **outside** the database. If the DB is dumped, the pepper should still be secret. Use environment variables, AWS Secrets Manager, or an HSM.

### 3. Using a fixed salt

Salts must be **unique per password**. Never hardcode a salt. Let the library generate it.

### 4. Not handling hash migration

When upgrading algorithms, existing users still need to log in. Use `passlib` with `deprecated="auto"` to re-hash on next login.

### 5. Timing attacks on verification

Always use the library's built-in `verify()` function — it uses constant-time comparison. Never compare hashes with `==`.

---

# Interview Questions

### Q1: "Why use Argon2id over bcrypt?"

**Answer:** Argon2id is memory-hard (resists GPU/ASIC cracking) and won the Password Hashing Competition (2015). bcrypt is CPU-only and vulnerable to FPGA attacks. Both are acceptable, but Argon2id is the current OWASP recommendation.

### Q2: "What's the difference between salt and pepper?"

**Answer:** **Salt** is unique per password, stored alongside the hash, prevents rainbow tables. **Pepper** is application-wide, stored outside the database, provides an additional layer if the DB is compromised.

### Q3: "Why not use SHA-256 with many iterations?"

**Answer:** SHA-256 is designed to be **fast**. Even with 100K iterations, a GPU can still compute millions of hashes per second. Argon2's memory-hardness makes each hash expensive in **both time and memory**, which GPUs cannot parallelize efficiently.

### Q4: "How do you migrate from bcrypt to Argon2id without forcing password resets?"

**Answer:** Use `passlib` with `deprecated="auto"`. On next login, verify with the old scheme (bcrypt), then re-hash with Argon2id and store the new hash. Gradual migration as users log in.

### Q5: "What are the recommended Argon2id parameters?"

**Answer:** OWASP suggests: `memory=19456 KB`, `iterations=2`, `parallelism=1`. Higher memory = more GPU resistance. Tune based on your server's available RAM and acceptable login latency (~0.5s).

---

## Related Notes

- [[Distributed System]] — security applies to distributed auth systems
- [[ETL]] — password data in ETL pipelines requires extra care (masking, encryption at rest)
- [[Python Environment Playbook]] — `argon2-cffi`, `bcrypt`, `passlib` setup