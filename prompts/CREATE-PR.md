---
tags: [git, workflow, pr]
---
# Create PR

Commit the current working changes, push the branch, and open a pull request with a clear description.

## Steps

1. Inspect state in parallel: `git status`, `git diff` (staged + unstaged), `git log --oneline -10`, and `git diff <base>...HEAD` (where `<base>` is `origin/main` or the repo's default branch).
2. Stage only files relevant to this change. Never blanket `git add -A` if there are unrelated artifacts in the tree. Never stage `.env`, credentials, lockfiles you didn't touch, or large binaries.
3. If on the default branch, create a new branch first. Name it kebab-case after the change (e.g. `fix-token-refresh`, `add-summary-prompt`).
4. Commit. Subject line under 72 chars, imperative mood, explains *why* over *what*. Body optional but useful when the diff doesn't speak for itself. Use a HEREDOC so formatting survives:

   ```bash
   git commit -m "$(cat <<'EOF'
   <subject>

   <optional body>
   EOF
   )"
   ```

5. Push with `-u` if the branch has no upstream.
6. Open the PR:

   ```bash
   gh pr create --title "<subject>" --body "$(cat <<'EOF'
   ## Summary
   - <bullet 1>
   - <bullet 2>

   ## Test plan
   - [ ] <how you verified>
   EOF
   )"
   ```

7. Return the PR URL.

## Rules

- Never `git push --force` to `main` or `master`.
- Never pass `--no-verify`, `--no-gpg-sign`, or `--amend` to a published commit.
- If a pre-commit hook fails, fix the underlying issue and create a *new* commit — do not amend.
- If the diff contains unrelated changes, stop and ask before bundling them.
- If there are no changes to commit, say so and exit — do not create an empty commit.
