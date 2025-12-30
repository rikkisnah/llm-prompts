#!/bin/bash
# getall - Pull latest updates for llm-prompts repository
# Compatible with Linux and macOS

set -euo pipefail

# Colors for output (using printf for portability)
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

printf "${BLUE}=== Pulling LLM Prompts Updates ===${NC}\n\n"

# Get current repository
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
printf "Updating: %s\n\n" "$(basename "$REPO_DIR")"

cd "$REPO_DIR"

# Stash any local changes
if git stash push -u -m "auto-stash $(date '+%Y-%m-%d_%H%M%S')" 2>&1 | grep -q "No local changes"; then
  printf "  No local changes to stash\n"
else
  printf "  Stashed local changes\n"
fi

# Pull with fast-forward only
if git pull --ff-only 2>/dev/null; then
  printf "  Successfully pulled latest changes\n"
else
  printf "  Note: Could not fast-forward (local changes exist or no remote)\n"
fi

printf "\n${GREEN}=== Update Complete ===${NC}\n"
