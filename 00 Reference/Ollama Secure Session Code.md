```table-of-contents
```

If you're trying to get the `__Secure-session` cookie **for your own authenticated Ollama account**, there are several legitimate ways. If the cookie is marked `HttpOnly` (which session cookies usually are), it **cannot be read with JavaScript** (`document.cookie`) by design. ([MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/Cookies?utm_source=chatgpt.com "Secure cookie configuration - Security | MDN"))

### Option 1: Chrome DevTools (Recommended)

1. Log in to `https://ollama.com`.
    
2. Open **Developer Tools** (`F12` or `Ctrl+Shift+I`).
    
3. Go to **Application** tab.
    
4. Expand **Storage → Cookies**.
    
5. Select `https://ollama.com`.
    
6. Find the cookie named:
    

```
__Secure-session
```

7. Double-click the **Value** column to copy it.
    

---

### Option 2: Network Tab

If the cookie is being sent with requests:

1. Open DevTools.
    
2. Go to **Network**.
    
3. Refresh the page.
    
4. Click a request to `ollama.com`.
    
5. Under **Request Headers**, look for
    

```
Cookie:
__Secure-session=xxxxxxxxxxxx
```

or under **Response Headers**

```
Set-Cookie:
__Secure-session=...
```

---

### Option 3: Chrome Cookie SQLite Database

Chrome stores cookies in its profile database.

**Windows**

```
%LOCALAPPDATA%\Google\Chrome\User Data\Default\Network\Cookies
```

However:

- Modern Chrome encrypts cookie values using OS-backed encryption.
    
- You cannot simply read the SQLite database to obtain the plaintext value without using Chrome or OS decryption APIs. ([MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie?utm_source=chatgpt.com "Set-Cookie header - HTTP | MDN"))
    

---

### Option 4: Browser Extensions

Extensions such as:

- Cookie-Editor
    
- EditThisCookie
    

can display cookies **only if the browser allows access**. If the cookie is `HttpOnly`, many extensions can still show it because they use the browser's cookies API rather than page JavaScript, subject to granted permissions.

---

### Option 5: Using Playwright

If you're already logged in:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir="C:/Users/<user>/AppData/Local/Google/Chrome/User Data",
        channel="chrome",
        headless=False
    )

    page = browser.new_page()
    page.goto("https://ollama.com/settings")

    cookies = browser.cookies()

    for cookie in cookies:
        if cookie["name"] == "__Secure-session":
            print(cookie["value"])
```

---

### Option 6: Using Selenium

Selenium can retrieve cookies after login:

```python
from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://ollama.com/settings")

# Log in manually

cookie = driver.get_cookie("__Secure-session")
print(cookie["value"])
```

---

### JavaScript won't work

This will likely return nothing:

```javascript
document.cookie
```

because `__Secure-session` is almost certainly set with the `HttpOnly` attribute, preventing access from JavaScript to protect against XSS attacks. ([MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/Cookies?utm_source=chatgpt.com "Secure cookie configuration - Security | MDN"))

---

### If your goal is to use the cookie in scripts or API requests

Let me know what you're trying to accomplish. For example:

- Python `requests`
    
- `curl`
    
- Postman
    
- Playwright
    
- Selenium
    
- Browser extension
    
- n8n
    

I can show the safest way to authenticate your own requests without exposing or mishandling your session cookie.
