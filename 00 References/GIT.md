**Best use case:**  
Distributed version control for tracking code changes, enabling branching/merging, and collaborating reliably across teams

**Alternative**: 
[[Perforce]] when handling very large binary assets or game development workflows

### 🔹 Common Commands

```bash
git init                # create a new repo
git clone <url>         # clone remote repo locally
git status              # see current changes
git add <file>          # stage file for commit
git commit -m "msg"     # commit staged changes
git branch              # list branches
git checkout <branch>   # switch branches
git merge <branch>      # merge a branch into current
git pull                # fetch + merge remote changes
git push                # upload local commits
git stash               # stash uncommitted changes
git rebase <branch>     # rebase current branch onto another
git log                 # view commit history
git reset --hard <sha>  # hard reset to commit
git revert <sha>        # create new commit undoing <sha>
git tag -a v1.0 -m "msg" # create annotated tag
```