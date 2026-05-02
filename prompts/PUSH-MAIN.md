---
tags: [git, workflow]
---
# Push to main

Commit the current working changes and push them straight to the default branch. Use this in solo repos with no branch protection. For collaborative repos, branch-protected repos, or anywhere a review trail matters, use `CREATE-PR.md` instead.

## Steps

1. Inspect state in parallel: `git status`, `git diff` (staged + unstaged), `git log --oneline -10`.
2. Confirm the current branch is the repo's default branch (`main` or `master`). If not, switch to it first or stop and ask.
3. Stage only files relevant to this change. Never blanket `git add -A` if there are unrelated artifacts in the tree. Never stage `.env`, credentials, lockfiles you didn't touch, or large binaries.
4. Commit. Subject line under 72 chars, imperative mood, explains *why* over *what*. Body optional but useful when the diff doesn't speak for itself. Use a HEREDOC so formatting survives:

   ```bash
   git commit -m "$(cat <<'EOF'
   <subject>

   <optional body>
   EOF
   )"
   ```

5. Pull with rebase: `git pull --rebase`. This rebases your new commit on top of any remote changes (for example, work pushed from another machine).
6. Push: `git push`.

## Rules

- Never `git push --force` to `main` or `master`.
- Never pass `--no-verify`, `--no-gpg-sign`, or `--amend` to a published commit.
- If a pre-commit hook fails, fix the underlying issue and create a *new* commit. Do not amend.
- If the diff contains unrelated changes, stop and ask before bundling them.
- If there are no changes to commit, say so and exit. Do not create an empty commit.
- If `git push` is rejected because the branch is protected, stop and switch to `CREATE-PR.md`. Do not try to bypass protection.
- If the rebase hits conflicts, stop and surface them to the user. Do not auto-resolve.
