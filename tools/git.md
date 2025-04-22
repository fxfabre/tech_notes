## Git

Tutorial git : https://learngitbranching.js.org/index.html
merge vs rebase : https://delicious-insights.com/fr/articles/bien-utiliser-git-merge-et-rebase/


##### Merge origin/master to current branch :
- git fetch origin
- git merge origin/master


##### Branches :
- `git checkout -b [name_of_your_new_branch]` : Create the branch on your local machine and switch in this branch
- `git checkout [name_of_branch]` : Change working branch
- `git push origin [name_of_your_branch]` : Push the branch
- `git remote add [name_of_your_remote] [name_of_your_branch]` : Add a new remote for your branch
- `git branch -d [name_of_your_new_branch]` : Delete a branch on your local filesystem


##### Tags :
- `git update-ref refs/tags/${tag_name} $commit_id` : lightweight tag
- `git tag -a v1.4 -m "my version 1.4" $commit_id` : Annotated tags, $commit_id optionnel, HEAD par défaut
- `git tag v1.4` : Lightweight tags
- `git tag -d $tag_id` : delete tag locally
- `git push origin --tags` : send local tags to server


##### Annuler un commit :
- `git reset --soft HEAD^` : Le dernier, en gardant les modif en local
- `git revert 42xxxxxxxxx` : Appliquer le commit inverse


##### Stash :
- `git stash list` : Liste tous les stash existant
- `git stash push -m "message"` : Stash tous les fichiers modifiés dans un nouveau stash
- `git stash push -m "message" -- path/to/file/to/include` : the path must be relative to the repository root, not to your current working dir.
- `git stash apply $stash_id` : Applique le stash en le gardant
- `git stash pop $stash_id` : Applique le stash et le supprime
- `git stash drop $stash_id` : supprime le stash


##### pre-commit Hooks :
https://pre-commit.com/
https://pre-commit.com/hooks.html
- `pip install pre-commit`
