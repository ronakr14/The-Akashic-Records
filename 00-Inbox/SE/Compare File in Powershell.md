---
domain: software-engineering
subdomain: powershell
note_type: tutorial
source_type: self
status: evergreen
level: intermediate
tags:
  - git-diff
  - file-comparison
  - cli2api
---
# AI Summary
A practical reference for comparing files in PowerShell across common scenarios. Covers line-by-line comparison with Compare-Object, file hash verification, binary comparison, JSON and CSV comparison, Git-based diffing with context, performance considerations, encoding caveats, and a decision matrix for selecting the best tool. Includes recommendations on when to use native PowerShell versus Git or external utilities for better readability and performance. 

---
# Quick & Dirty (Line-by-Line Diff)

If you just want to know “what changed” between two text files:
```powershell
Compare-Object (Get-Content file1.txt) (Get-Content file2.txt)
```

## Output meaning:
- `<=` → only in file1    
- `=>` → only in file2    

👉 Add more clarity:
```powershell
Compare-Object (Get-Content file1.txt) (Get-Content file2.txt) -IncludeEqual
```

Tip: `diff` is a built-in alias for `Compare-Object` in PowerShell. Use whichever you prefer.

---
# 🔍 2. Side-by-Side Feel (Better Readability)

```powershell
Compare-Object (Get-Content file1.txt) (Get-Content file2.txt) |
Format-Table
```
Still basic, but cleaner.

---
# ⚡ 3. Show Line Numbers (Actually Useful)

Default diff is blind — no line numbers. Fix that:
```powershell
$file1 = Get-Content file1.txt
$file2 = Get-Content file2.txt

Compare-Object $file1 $file2 -PassThru |
ForEach-Object {
    [PSCustomObject]@{
        Line      = $_
        InFile1   = $file1 -contains $_
        InFile2   = $file2 -contains $_
    }
}
```
Not perfect (duplicates can mess it up), but better for real work.

---

# 🧪 4. Exact Match Check (Binary Level)

If your question is just:
> “Are these files identical?”

```powershell
Get-FileHash file1.txt
Get-FileHash file2.txt
```
Compare hashes. If same → files are identical.

⚠️ Encoding caveat: `Get-Content` defaults to UTF-8. For ANSI or BOM-encoded files, specify encoding:
```powershell
Get-Content file1.txt -Encoding UTF8
```

---

# 📦 5. Binary / Large File Compare

PowerShell is slow for large files. Use the native Windows `fc` command:

```powershell
fc /b file1.bin file2.bin
```

`/b` = binary mode. Output is minimal — just shows differing byte offsets. Much faster than `Compare-Object` on files >100MB.

Alternative: `cmp` (available in Git Bash / WSL):
```bash
cmp file1.bin file2.bin
```

---

# 🧱 6. Structured Files (JSON / CSV)

Now we’re talking real engineering use cases.
## JSON compare:
```powershell
Compare-Object `
    (Get-Content file1.json | ConvertFrom-Json) `
    (Get-Content file2.json | ConvertFrom-Json)
```

⚠️ Caveat: Works only if structure aligns. Otherwise, it gets messy fast.

---

## CSV compare:

```powershell
Compare-Object `
    (Import-Csv file1.csv) `
    (Import-Csv file2.csv)
```
👉 Add `-Property` for meaningful comparison:
```powershell
Compare-Object `
    (Import-Csv file1.csv) `
    (Import-Csv file2.csv) `
    -Property ID, Name
```

---
# 🚀 7. When PowerShell Isn't Enough (Real Talk)

PowerShell diff is… serviceable. Not great.
If you care about:
- large files    
- readable diffs    
- merge workflows    

Use:
- `git diff` (even outside Git repos)    
- VS Code compare    
- tools like WinMerge    

Example:
```powershell
git diff --no-index file1.txt file2.txt
```
👉 This is honestly the **pro move**.

---

# 📊 8. Context Diff (Show Surrounding Lines)

`git diff` supports unified diff with context:

```powershell
git diff -U5 file1.txt file2.txt
```

`-U5` = show 5 lines of context around each change. Use `-U0` for no context, `-U10` for more.

If you don't have Git installed, `Compare-Object` can't do this — another reason `git diff --no-index` is strictly better.

---

# 🧭 Quick Decision Matrix

| Scenario | Command | Notes |
|---|---|---|
| Quick text diff | `diff file1.txt file2.txt` | Alias for Compare-Object |
| See which lines are equal too | `diff file1.txt file2.txt -IncludeEqual` | Adds `==` marker |
| Side-by-side view | `diff file1.txt file2.txt \| Format-Table` | Cleaner output |
| Just check if identical | `(Get-FileHash file1.txt).Hash -eq (Get-FileHash file2.txt).Hash` | Boolean result |
| Large/binary files | `fc /b file1.bin file2.bin` | Native, fast |
| JSON with structure | `diff (Get-Content f1.json \| ConvertFrom-Json) (Get-Content f2.json \| ConvertFrom-Json)` | Structure-aware |
| Need context lines | `git diff -U5 file1.txt file2.txt` | Best readability |

---

# 🧭 My Straight Take

- Need quick diff → `Compare-Object`   
- Need accuracy → `Get-FileHash`    
- Need sanity → use `git diff`    

PowerShell gets the job done, but it's not a world-class diff tool.

---

## Related Notes

- [[Git Multi Account Setup]] — git diff requires git config
- [[VSCode Debug]] — VS Code has built-in file compare
- [[Python Environment Playbook]] — Python's `difflib` for programmatic comparison
- [[BitRouter]] — tool selection heuristics apply here too
