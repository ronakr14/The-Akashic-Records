```table-of-contents
```
# 🧠 1. Quick & Dirty (Line-by-Line Diff)

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

---

# 🧱 5. Structured Files (JSON / CSV)

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
# 🚀 6. When PowerShell Isn’t Enough (Real Talk)

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

# 🧭 My Straight Take

- Need quick diff → `Compare-Object`   
- Need accuracy → `Get-FileHash`    
- Need sanity → use `git diff`    

PowerShell gets the job done, but it’s not a world-class diff tool.
