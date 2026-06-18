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