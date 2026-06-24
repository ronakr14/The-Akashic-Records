---
type: project
---

# PowerShell Profile Customisation

```table-of-contents
```

## What Is a PowerShell Profile?

A PowerShell profile is a script that runs automatically when you open a new PowerShell session. It's useful for:

- Customising the prompt
- Setting aliases and functions
- Exporting modules
- Defining environment variables

## Locate Your Profile

```powershell
$PROFILE
```

This returns the path to your profile file. The file does not exist by default — you must create it.

Common locations:

| Scope | Path |
|---|---|
| Current user, current host | `$PROFILE` |
| Current user, all hosts | `$PROFILE.CurrentUserAllHosts` |
| All users, current host | `$PROFILE.AllUsersCurrentHost` |

## Create the Profile File

```powershell
New-Item -ItemType File -Path $PROFILE -Force
```

## Edit the Profile

```powershell
notepad $PROFILE
```

Or use any editor:

```powershell
code $PROFILE
```

## Common Customisations

### Short Prompt

Show only the current folder name instead of the full path:

```powershell
function prompt {
    "$(Split-Path -Leaf (Get-Location)) > "
}
```

### Useful Aliases

```powershell
Set-Alias ll Get-ChildItem
Set-Alias grep Select-String
Set-Alias which Get-Command
```

### Auto-Load Modules

```powershell
Import-Module posh-git
Import-Module oh-my-posh
```

### Environment Variables

```powershell
$env:EDITOR = "code"
```

### Custom Functions

```powershell
function reload { . $PROFILE }
```

Adds a `reload` command to re-source the profile without restarting the terminal.

## Apply Changes

After editing, either restart PowerShell or re-source:

```powershell
. $PROFILE
```

## Troubleshooting

| Issue | Fix |
|---|---|
| Profile doesn't run | Check execution policy: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Script blocked | Sign the file or lower execution policy |
| Changes not visible | Run `. $PROFILE` to re-source |
