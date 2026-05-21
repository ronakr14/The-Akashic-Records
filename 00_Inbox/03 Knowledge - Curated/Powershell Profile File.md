
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
