---
name: create-pr
description: "Automatically prepare local pull request work from repository changes. Use when the user asks to create a PR, prepare a PR, commit current changes for review, generate a meaningful PR branch and commit, or produce a PR description without pushing to a remote."
---

<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Create PR

Use this skill to inspect changed files, choose the correct local branch, commit the appropriate changes locally, and show a PR description that matches the project structure and review expectations.

## Operating Rules

- Default to an automatic local workflow: inspect changes, select or create the local branch, commit locally, then print a PR description.
- Never push to a remote. Do not run `git push`, `gh pr create`, or any command that publishes the branch or opens a remote PR.
- Ask concise questions only when automatic local preparation would include uncertain changes or cannot proceed safely.
- Inspect the repository before drafting: read root instructions, README files, PR templates, package metadata, build files, and nearby tests when they exist.
- Treat project-local instructions as authoritative over generic PR conventions.
- Preserve user changes. Do not revert unrelated work, rewrite history, force-push, delete branches, or run destructive cleanup unless explicitly requested.
- Verify the active branch, base branch, and working tree before selecting a branch or committing.
- If the current checkout is a linked Git worktree, use the worktree's current branch and do not create another branch.
- If the current branch is `main`, `master`, or the repository default branch, create a meaningful local branch before committing.
- If the current branch is already a feature or worktree branch, use that branch.
- Generate new branch names and commit messages from the actual diff, using short lowercase hyphenated branch names.
- Use `git commit -am "..."` for tracked modified or deleted files. This does not include untracked files; ask before staging untracked files.
- Call out changed files that were not touched by the current assistant session when that information is available. Ask the user whether to include them; if they say yes, redo the local branch, commit, and PR description flow.
- Do not invent issue IDs, reviewers, test results, risk details, or deployment notes. Write `insufficient data` where evidence is unavailable.

## Workflow

1. Inspect project structure and conventions:
   - Read `AGENTS.md`, `CLAUDE.md`, `.github/pull_request_template*`, `README.md`, `CONTRIBUTING.md`, `Makefile`, package files, and CI config when present.
   - Identify the project type, test commands, formatting commands, and PR body requirements from local evidence.
   - Use `rg --files` and focused reads instead of broad directory dumps.
2. Inspect all changed files:
   - Run `git status --short`, `git branch --show-current`, `git diff --name-status`, `git diff --stat`, and focused diffs.
   - Include staged and unstaged tracked changes in the review. Inspect untracked files separately with `git status --short`.
   - If there are no changed files, stop and report that there is nothing to prepare.
3. Check file ownership for this session:
   - Compare changed files with files touched by the current assistant session when the session history provides that evidence.
   - If changed files were not touched by this session, list them and ask whether to include them before committing.
   - If session ownership cannot be determined, state `insufficient data` and proceed only with changes that are clearly part of the user's requested work.
4. Select or create the local branch:
   - Run `git branch --show-current`, `git rev-parse --git-dir`, and `git rev-parse --git-common-dir`.
   - Treat the checkout as a linked worktree when the Git directory differs from the common directory and the Git directory path includes `worktrees`.
   - If this is a linked worktree, keep the current branch and continue. Do not create another branch.
   - If the current branch is `main`, `master`, or the detected default branch, create a new branch before committing.
   - If the current branch is already a feature branch, keep using it.
   - Summarize the diff into a short action phrase.
   - For new branches, create a name such as `codex/add-pr-skill` or `codex/update-create-pr-workflow`.
   - If the branch already exists, add a short numeric suffix instead of overwriting it.
   - Use `git switch -c <branch-name>` only when creating a branch.
5. Commit local changes:
   - For tracked modified or deleted files, run `git commit -am "<meaningful message>"`.
   - For untracked files, ask before staging them. If the user approves, run `git add <paths>` and then `git commit -m "<meaningful message>"`.
   - If the user changes the included file set after review, redo the branch, commit, and PR description steps from the new selected set.
   - Do not run any remote push command.
6. Validate appropriately:
   - Run project-specified validation commands when feasible and relevant.
   - If validation cannot run, explain the blocker and mark the result as `not run`.
   - Do not claim successful validation without command output.
7. Show the PR description:
   - Use the repository's PR template when present.
   - Write a concise imperative title.
   - Summarize what changed and why.
   - Include validation commands and results.
   - Include risks, rollout notes, screenshots, or follow-ups only when supported by evidence or requested by the template.
   - Make clear that the PR was not pushed or opened remotely.

## Command Patterns

Use these as starting points and adapt to project instructions:

```bash
git status --short
git branch --show-current
git rev-parse --git-dir
git rev-parse --git-common-dir
git diff --name-status
git diff --stat
git diff
git switch -c codex/meaningful-branch-name
git commit -am "Meaningful commit message"
git add path/to/approved-untracked-file
git commit -m "Meaningful commit message"
```

## Output Contract

- State the local branch name and commit hash.
- Include the changed files reviewed and any files excluded from the commit.
- Call out changed files not touched by the current assistant session, or state `insufficient data` if session ownership cannot be determined.
- Include the PR title and PR description.
- Include validation commands run and their results.
- Explicitly state that no remote push or remote PR creation was performed.
- List assumptions, missing data, and any user decisions still needed.
