---
domain: software-engineering
subdomain: fastapi
note_type: tutorial
source_type: self
status: evergreen
level: intermediate
tags:
  - jwt
  - authentication
  - ai-security
---
# AI Sumamry
Comprehensive FastAPI authentication guide covering common authentication mechanisms, JWT bearer token architecture, password hashing with bcrypt, OAuth2 integration, login implementation, token creation and validation, dependency-based route protection, role-based authorization, refresh token strategy, production security best practices, recommended project structure, and libraries for authentication. Concludes with a scalable production architecture using JWT access and refresh tokens, PostgreSQL, dependency injection, and environment-based configuration for secure backend APIs.

---

Authentication in FastAPI depends on **who is calling your API**. There is no single "FastAPI auth." Instead, FastAPI provides building blocks, and you choose the appropriate authentication mechanism.

---

# Authentication Options

|Method|Best For|Stateful|Difficulty|
|---|---|---|---|
|API Key|Internal services|No|Easy|
|JWT (OAuth2 Password Bearer)|Web apps, SPAs, mobile|No|Medium|
|Session Cookies|Traditional websites|Yes|Medium|
|OAuth (Google/GitHub/Azure)|Social login, enterprise|Usually No|Hard|
|Basic Auth|Internal tools only|No|Easy|
|mTLS|Highly secure service-to-service|No|Hard|

For most modern REST APIs:

> **JWT Bearer Tokens** are the standard.

---

# Typical Architecture

```
            Login
Client ----------------> FastAPI
                          |
                    Verify username/password
                          |
                    Create JWT Token
                          |
<------------------------- token

Subsequent requests

Client
Authorization: Bearer eyJhbG...

                |
                V

FastAPI
Verify JWT
Load User
Execute endpoint
```

---

# Recommended Project Structure

```
app/
│
├── auth/
│   ├── jwt.py
│   ├── security.py
│   ├── dependencies.py
│   └── password.py
│
├── routers/
│   ├── users.py
│   └── auth.py
│
├── models/
├── services/
└── main.py
```

---

# Step 1: Install Packages

```bash
pip install python-jose[cryptography]
pip install passlib[bcrypt]
pip install python-multipart
```

---

# Step 2: Hash Passwords

Never store passwords.

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)
```

Store only:

```
$2b$12$Y...
```

Never:

```
password123
```

---

# Step 3: Configure JWT

```python
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

Create token:

```python
def create_access_token(data: dict):
    payload = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=30)

    payload["exp"] = expire

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
```

---

# Step 4: Login Endpoint

```python
@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):

    user = authenticate_user(
        form.username,
        form.password,
    )

    if not user:
        raise HTTPException(401)

    token = create_access_token(
        {"sub": user.username}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
```

Response

```json
{
  "access_token":"eyJhbGc...",
  "token_type":"bearer"
}
```

---

# Step 5: Read Token

FastAPI includes OAuth2 helpers.

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
```

Now create dependency.

```python
from jose import jwt

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    username = payload["sub"]

    return get_user(username)
```

---

# Step 6: Protect Routes

```python
@app.get("/profile")
def profile(
    current_user=Depends(get_current_user)
):
    return current_user
```

Now this endpoint requires:

```
Authorization: Bearer <token>
```

---

# Step 7: Role-Based Authorization

JWT

```json
{
  "sub":"ronak",
  "role":"admin"
}
```

Dependency

```python
def require_admin(
    user=Depends(get_current_user)
):
    if user.role != "admin":
        raise HTTPException(403)
    return user
```

Use

```python
@app.delete("/users")
def delete_users(
    admin=Depends(require_admin)
):
    ...
```

---

# API Flow

```
POST /login

↓

username/password

↓

Verify

↓

JWT

↓

Client stores JWT

↓

Authorization: Bearer token

↓

FastAPI verifies JWT

↓

Current User

↓

Endpoint
```

---

# Refresh Tokens

Access tokens should be short-lived (e.g., 15–30 minutes).

Use a longer-lived refresh token.

```
Login

↓

Access Token
15 min

↓

Refresh Token
30 days

↓

POST /refresh

↓

New Access Token
```

This lets users stay logged in without making access tokens long-lived.

---

# Security Best Practices

- Use HTTPS in production.
    
- Store passwords with bcrypt or Argon2 (never plaintext).
    
- Keep access tokens short-lived.
    
- Use refresh tokens for long sessions.
    
- Store secrets in environment variables, not source code.
    
- Validate issuer (`iss`) and audience (`aud`) claims if tokens are used across multiple services.
    
- Rotate signing keys periodically.
    
- Return generic login errors ("Invalid username or password") to avoid revealing which usernames exist.
    

---

# Libraries Worth Considering

Instead of implementing everything yourself, these libraries provide production-ready user management:

- [FastAPI Users](https://fastapi-users.github.io/fastapi-users/?utm_source=chatgpt.com) — complete authentication, registration, password reset, OAuth providers, JWT, and database integrations.
    
- [Authlib](https://docs.authlib.org/?utm_source=chatgpt.com) — OAuth 2.0 and OpenID Connect support for integrating with Google, GitHub, Microsoft Entra ID, etc.
    
- [python-jose](https://python-jose.readthedocs.io/?utm_source=chatgpt.com) — JWT creation and validation.
    
- [pwdlib](https://frankie567.github.io/pwdlib/?utm_source=chatgpt.com) — modern password hashing library (also supported by FastAPI examples).
    

---

# Recommendation for Your Stack

Given your background in Data Engineering and your work on FastAPI backends, I'd use:

- **Authentication:** JWT access tokens + refresh tokens.
    
- **Password hashing:** Argon2 (or bcrypt if compatibility is required).
    
- **Database:** Store users and refresh tokens in PostgreSQL.
    
- **Authorization:** FastAPI dependency injection with role/permission checks.
    
- **Configuration:** Load secrets from environment variables via Pydantic Settings.
    
- **Future scalability:** If you later split into multiple services, issue JWTs from a dedicated authentication service or an identity provider (such as Keycloak or Microsoft Entra ID) while each service verifies the tokens independently.
    

This architecture is stateless, scales well behind load balancers, and aligns with common production deployments of FastAPI APIs.
