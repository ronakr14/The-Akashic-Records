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