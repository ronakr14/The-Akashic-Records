#git #multi-account #set-up
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

Create two identity files: Choose your location
### 📄 `<location>/.gitconfig-personal` 

```ini
[user]
    name = Your Name
    email = your_personal@email.com
```

### 📄 `<location>/.gitconfig-work` 

```ini
[user]
    name = Your Work Name
    email = your_work@email.com
```

---

## 🎯 Step 3: Auto-switch based on folder (THIS is the power move)

Edit your main config:
```bash
# linux
nano ~/.gitconfig

# windows:
notepad $HOME\.gitconfig
```

Add:
```ini
# linux
[includeIf "gitdir:~/projects/personal/"]
    path = <location>/.gitconfig-personal

[includeIf "gitdir:~/projects/work/"]
    path = <location>/.gitconfig-work
    
# windows:
[includeIf "gitdir/i:<location from root>/personal/"]
    path = <location>/.gitconfig-personal

[includeIf "gitdir/i:<location from root>/work/"]
    path = <location>/.gitconfig-work
```

 What this does:
- Any repo inside `~/projects/personal/` → uses personal identity    
- Any repo inside `~/projects/work/` → uses work identity    
- `gitdir/i:` for case insensitive on windows
- trailing slash matters for project folders
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

Then configure `~/.ssh/config` or `$HOME\.ssh\config`:
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

Add Public Keys to GitHub, Get personal public key:
windows:
```powershell
Get-Content $HOME\.ssh\id_ed25519_personal.pub
Get-Content $HOME\.ssh\id_ed25519_work.pub
```

Clone like:
```bash
git clone git@github-work:company/repo.git
git clone git@github-personal:username/repo.git
```
