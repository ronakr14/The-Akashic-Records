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



Yep — that guide is heavily Linux/macOS-centric. On Windows + PowerShell, the concepts are still correct, but:

- paths are different
    
- `nano`, `chmod`, `mkdir -p`, `~/.ssh/config` assumptions break
    
- Git config files are hidden in Windows user profile folders
    
- some shell scripts need PowerShell equivalents
    

Let’s modernize this properly for **Windows + PowerShell + Git for Windows** using official Git/GitHub behavior.

---

# First: Where are Git config files on Windows?

Git on Windows stores configs here:

|Scope|Location|
|---|---|
|Global user config|`C:\Users\<YOU>\.gitconfig`|
|Repo/local config|`<repo>\.git\config`|
|Git system config|`C:\Program Files\Git\etc\gitconfig`|

So your Linux:

```bash
~/.gitconfig
```

Becomes:

```powershell
$HOME\.gitconfig
```

To open it:

```powershell
notepad $HOME\.gitconfig
```

Or VS Code:

```powershell
code $HOME\.gitconfig
```

Much easier than hunting hidden files manually.

---

# Recommended Windows Setup (Simple + Reliable)

This is the cleanest setup for:

- personal GitHub
    
- work GitHub
    
- automatic switching
    
- minimal maintenance
    
- zero accidental commits
    

---

# Step 1 — Set Personal Identity as Global Default

Run in PowerShell:

```powershell
git config --global user.name "Your Name"
git config --global user.email "personal@email.com"
```

Verify:

```powershell
git config --global --list
```

Or individually:

```powershell
git config user.name
git config user.email
```

---

# Step 2 — Create Separate Identity Files

Create these files:

```powershell
notepad $HOME\.gitconfig-personal
```

Paste:

```ini
[user]
    name = Your Name
    email = personal@email.com
```

Now work identity:

```powershell
notepad $HOME\.gitconfig-work
```

Paste:

```ini
[user]
    name = Your Work Name
    email = work@company.com
```

Save both.

---

# Step 3 — Configure Auto-Switching (The Important Part)

Open main config:

```powershell
notepad $HOME\.gitconfig
```

Add this at bottom:

```ini
[includeIf "gitdir/i:C:/Users/YOUR_USERNAME/projects/personal/"]
    path = C:/Users/YOUR_USERNAME/.gitconfig-personal

[includeIf "gitdir/i:C:/Users/YOUR_USERNAME/projects/work/"]
    path = C:/Users/YOUR_USERNAME/.gitconfig-work
```

## Important details

### `gitdir/i:`

- `i` = case insensitive
    
- recommended on Windows
    

### Use forward slashes

Git prefers:

```ini
C:/Users/name/
```

NOT:

```ini
C:\Users\name\
```

### Trailing slash matters

This:

```ini
projects/work/
```

works correctly.

Without trailing slash, Git matching can fail unexpectedly.

---

# Step 4 — Create Folder Structure

PowerShell equivalent of `mkdir -p`:

```powershell
mkdir "$HOME\projects\personal"
mkdir "$HOME\projects\work"
```

Or shorter:

```powershell
md "$HOME\projects\personal"
md "$HOME\projects\work"
```

---

# Step 5 — Clone Repos into Correct Folders

Example:

```powershell
cd "$HOME\projects\work"
git clone git@github-work:company/repo.git
```

Personal:

```powershell
cd "$HOME\projects\personal"
git clone git@github-personal:your/repo.git
```

---

# Step 6 — Verify Auto Switching

Inside repo:

```powershell
git config user.name
git config user.email
```

You should see correct identity automatically.

If not:

- repo location is wrong
    
- path matching in `.gitconfig` is wrong
    
- trailing slash missing
    

Usually one of those three.

---

# SSH Setup for Multiple GitHub Accounts (Strongly Recommended)

This is where most people create chaos accidentally.

---

# Step 7 — Generate Separate SSH Keys

Personal:

```powershell
ssh-keygen -t ed25519 -C "personal@email.com"
```

When asked filename:

```text
C:\Users\YOU\.ssh\id_ed25519_personal
```

Work:

```powershell
ssh-keygen -t ed25519 -C "work@company.com"
```

Filename:

```text
C:\Users\YOU\.ssh\id_ed25519_work
```

---

# Step 8 — Create SSH Config

Open:

```powershell
notepad $HOME\.ssh\config
```

Paste:

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

---

# Step 9 — Add Public Keys to GitHub

Get personal public key:

```powershell
Get-Content $HOME\.ssh\id_ed25519_personal.pub
```

Work:

```powershell
Get-Content $HOME\.ssh\id_ed25519_work.pub
```

Add them to:

- personal GitHub account
    
- work GitHub account
    

at:

[GitHub SSH Keys Settings](https://github.com/settings/keys?utm_source=chatgpt.com)

Official GitHub docs:

[GitHub SSH Authentication Docs](https://docs.github.com/en/authentication/connecting-to-github-with-ssh?utm_source=chatgpt.com)

---

# Step 10 — Clone Using SSH Aliases

Work:

```powershell
git clone git@github-work:company/repo.git
```

Personal:

```powershell
git clone git@github-personal:yourusername/repo.git
```

That alias routing is what selects the right SSH key automatically.

This is the part most tutorials explain badly.

---

# Simpler Alternative (Honestly Fine for Most People)

If all this feels over-engineered:

You can skip separate `.gitconfig-*` files entirely and just use per-repo config:

Inside work repo:

```powershell
git config user.name "Work Name"
git config user.email "work@company.com"
```

Inside personal repo:

```powershell
git config user.name "Personal Name"
git config user.email "personal@email.com"
```

That stores config in:

```text
repo/.git/config
```

Pros:

- dead simple
    
- reliable
    
- no includeIf complexity
    

Cons:

- manual setup per repo
    

For most developers with:

- 1 work org
    
- 1 personal account
    

…this is honestly enough.

---

# About Hooks on Windows

Your original hook script is Bash.

Git for Windows CAN run Bash hooks because Git ships with:

```text
C:\Program Files\Git\bin\bash.exe
```

So technically it works.

BUT:

- path matching becomes annoying
    
- Windows path separators create edge cases
    
- debugging hooks becomes pain
    

My recommendation:

- skip hooks initially
    
- use folder-based auto-switching
    
- verify identity before first few commits
    
- once stable, THEN add enforcement
    

Because complexity compounds fast.

---

# Useful Debug Commands

See where config comes from:

```powershell
git config --list --show-origin
```

This is insanely useful.

You’ll see:

```text
file:C:/Users/you/.gitconfig
file:C:/Users/you/.gitconfig-work
```

That immediately tells you whether include rules worked.

---

# Official References

Git official config docs:

[Git Config Documentation](https://git-scm.com/docs/git-config?utm_source=chatgpt.com)

Conditional includes:

[Git Conditional Includes Documentation](https://git-scm.com/docs/git-config?utm_source=chatgpt.com#_conditional_includes)

GitHub SSH setup:

[GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh?utm_source=chatgpt.com)

---

# My recommendation for your actual setup

Do this stack:

## Minimum viable professional setup

- Separate SSH keys
    
- Folder-based includeIf
    
- Organized repo folders
    

Skip:

- hooks
    
- fancy automation
    
- commit enforcement
    

Until you’ve used the setup for a week.

Because operational simplicity beats “clever infrastructure” every time.