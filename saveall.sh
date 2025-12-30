#!/bin/bash
# saveall - Save LLM prompts and sync with GitHub
# Compatible with Linux and macOS

set -e  # Exit on error

# Colors for output (using printf for portability)
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

printf "${BLUE}=== LLM Prompts Sync ===${NC}\n"
printf "Repository: llm-prompts\n"
printf "Host: %s\n" "$(hostname)"
printf "Time: %s\n\n" "$(date '+%Y-%m-%d %H:%M:%S')"

# Change to script directory
cd "$(dirname "$0")"

# Check for uncommitted changes
printf "${BLUE}Checking for changes...${NC}\n"
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    printf "No changes to commit\n"
else
    printf "Changes detected\n"

    # Stage all changes
    printf "${BLUE}Staging changes...${NC}\n"
    git add -A

    # Get diff summary for commit message
    DIFF_SUMMARY=$(git diff --cached --stat)

    # Create commit message with timestamp and change summary
    COMMIT_MSG="LLM prompts update: $(date '+%Y-%m-%d %H:%M:%S') from $(hostname)

Summary of changes:
$DIFF_SUMMARY"

    # Commit
    printf "${BLUE}Committing changes...${NC}\n"
    git commit -m "$COMMIT_MSG"
fi

# Pull latest from remote (rebase to avoid merge commits)
printf "${BLUE}Pulling latest from remote...${NC}\n"
git pull --rebase 2>/dev/null || printf "No remote configured or unable to pull\n"

# Push to GitHub
printf "${BLUE}Pushing to GitHub...${NC}\n"
git push || printf "No remote configured or unable to push\n"

printf "${GREEN}✓ LLM prompts synced${NC}\n"
