
# Check where the profile should exist
Run: `$PROFILE`
It will return something like:
```
C:\Users\ronak.rathore.ASCENDION\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
```
That file **does not exist yet**, which is why you can’t edit it.

---

# Create the profile file
Run this:
```powershell
New-Item -ItemType File -Path $PROFILE -Force
```
PowerShell will create the file.

---
# Open it
```powershell
notepad $PROFILE
```


1. Open your PowerShell profile:  `notepad $PROFILE`
2. Add this inside:
```powershell
function prompt {
    "$(Split-Path -Leaf (Get-Location)) > "
}
```

3. Save and restart PowerShell.   
Now every terminal will use the short prompt.


---
id: dg7q6tat7d2pmnjau7wjcrc
title: Windows
desc: ''
updated: 1753022796760
created: 1753022755822
---

## 🚀 Steps to Auto-Run Commands in PowerShell Terminal

### 1️⃣ **Check if You Have a Profile File**

```powershell
Test-Path $PROFILE
```

* **If it returns `False`**, create it:

```powershell
New-Item -Path $PROFILE -ItemType File -Force
```

---

### 2️⃣ **Edit Your Profile File**

This is where you add your startup commands.

```powershell
notepad $PROFILE
```

Add your commands in this file. Example:

```powershell
# Example commands
Set-Location C:\Projects\DefaultFolder
Import-Module posh-git
Write-Host "Ready to code, boss!" -ForegroundColor Green
```

---

### 3️⃣ **Save and Restart PowerShell**

Every new terminal session will now execute whatever you placed inside `$PROFILE`.

---

## ⚡ Pro Tip: Multiple Profiles

PowerShell distinguishes between:

* **Current User / Current Host** (`$PROFILE`)
* **All Users / Current Host** (`$PROFILE.AllUsersCurrentHost`)
* **Current User / All Hosts** (`$PROFILE.CurrentUserAllHosts`)
* **All Users / All Hosts** (`$PROFILE.AllUsersAllHosts`)

You likely only need:

```powershell
$PROFILE.CurrentUserCurrentHost
```

But for enterprise-wide configs, administrators can target the "All Users" profiles.

---

## 🛑 Important Gotcha: Execution Policy

If scripts aren't running due to policy restrictions:

```powershell
Get-ExecutionPolicy
```

If it's `Restricted`, loosen it (only if you trust your environment):

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🛠️ Example Use Case

Auto-connect to Azure, Git, or AWS CLI profiles, preload virtual environments, or set working directories—all automated.

---

Need help writing a specific startup script? Tell me what exact commands or tools you're using, and I’ll mock up a ready-to-paste profile for you.
