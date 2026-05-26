```table-of-contents
```
# Defaults
## 🚀 Set global username and global email

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

## 🔍 Verify it (don’t skip this)

```bash
git config --global --list
git config --global user.name
git config --global user.email
```
---

# Multi Account Setup
## ⚙️ Step 1: Set a safe default (global config)

Make your **global identity your personal one** (lowest risk baseline):
```bash
git config --global user.name "Your Name"
git config --global user.email "your_personal@email.com"
```

---

## 🗂️ Step 2: Create separate config files

Create two identity files:
### 📄 `~/.gitconfig-personal`

```ini
[user]
    name = Your Name
    email = your_personal@email.com
```

### 📄 `~/.gitconfig-work`

```ini
[user]
    name = Your Work Name
    email = your_work@email.com
```

---

## 🎯 Step 3: Auto-switch based on folder (THIS is the power move)

Edit your main config:
```bash
nano ~/.gitconfig
```

Add:
```ini
[includeIf "gitdir:~/projects/personal/"]
    path = ~/.gitconfig-personal

[includeIf "gitdir:~/projects/work/"]
    path = ~/.gitconfig-work
```

 What this does:
- Any repo inside `~/projects/personal/` → uses personal identity    
- Any repo inside `~/projects/work/` → uses work identity    

👉 Translation: zero manual switching. System handles it.

---

## 📁 Step 4: Organize your repos (non-negotiable)

Structure matters. Do this:

```bash
mkdir -p ~/projects/personal
mkdir -p ~/projects/work
```

Clone accordingly:

```bash
cd ~/projects/work
git clone <company-repo>

cd ~/projects/personal
git clone <your-repo>
```

---

## 🔍 Step 5: Verify before you commit (habit > regret)

Inside any repo:

```bash
git config user.name
git config user.email
```

---

## 🔐 Bonus: SSH separation (next-level clean setup)

If you use multiple GitHub accounts, create separate SSH keys:

```bash
ssh-keygen -t ed25519 -C "your_personal@email.com"
ssh-keygen -t ed25519 -C "your_work@email.com"
```

Then configure `~/.ssh/config`:
```ini
Host github-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_personal

Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_work
```

Clone like:
```bash
git clone git@github-work:company/repo.git
git clone git@github-personal:username/repo.git
```

---
# Multi Account Setup - using Hooks
## ⚙️ Step 1: Create a global hooks directory

```bash
mkdir -p ~/.githooks
git config --global core.hooksPath ~/.githooks
```

👉 This makes Git use your custom hooks for **every repo**.

---

## 🛑 Step 2: Create the pre-commit hook

```bash
nano ~/.githooks/pre-commit
```

Paste this:

```bash
#!/bin/bash

# Get current repo path
REPO_PATH=$(pwd)

# Get current git email
CURRENT_EMAIL=$(git config user.email)

# Define expected emails
WORK_EMAIL="your_work@email.com"
PERSONAL_EMAIL="your_personal@email.com"

# Define folder rules
if [[ "$REPO_PATH" == *"/projects/work/"* ]]; then
    EXPECTED_EMAIL=$WORK_EMAIL
elif [[ "$REPO_PATH" == *"/projects/personal/"* ]]; then
    EXPECTED_EMAIL=$PERSONAL_EMAIL
else
    echo "⚠️ Unknown repo location. Commit blocked."
    exit 1
fi

# Validate email
if [ "$CURRENT_EMAIL" != "$EXPECTED_EMAIL" ]; then
    echo "❌ ERROR: Wrong Git email detected!"
    echo "Expected: $EXPECTED_EMAIL"
    echo "Found:    $CURRENT_EMAIL"
    echo "Fix it before committing."
    exit 1
fi

echo "✅ Git identity check passed."
exit 0
```

---

## 🔐 Step 3: Make it executable

```bash
chmod +x ~/.githooks/pre-commit
```

---

## 🔍 Step 4: Test it (don’t skip)

Go into a repo and intentionally mess it up:

```bash
git config user.email "wrong@email.com"
git commit -m "test"
```

👉 It should block you. If it doesn’t, something’s off.

---

## 💡 Optional upgrade (highly recommended)

### Add username validation too

Modify script:

```bash
CURRENT_NAME=$(git config user.name)

WORK_NAME="Your Work Name"
PERSONAL_NAME="Your Name"
```

Then validate same way as email.

---

# ⚠️ Brutal truth

Without this:
- You rely on memory (bad system)    
- You will slip (guaranteed)    
- Cleanup later = annoying + visible    

With this:
- You get **zero-error commits**    
- You operate like someone who respects their own systems    

---

## 🧭 Final setup architecture (clean AF)

- Global config → default identity    
- Folder-based config → auto-switch    
- SSH split → account isolation    
- Hooks → enforcement layer    

👉 That’s a production-grade personal workflow.
