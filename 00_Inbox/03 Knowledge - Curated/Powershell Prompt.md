1. Open your PowerShell profile:  `notepad $PROFILE`
2. Add this inside:
```powershell
function prompt {
    "$(Split-Path -Leaf (Get-Location)) > "
}
```

3. Save and restart PowerShell.   
Now every terminal will use the short prompt.
