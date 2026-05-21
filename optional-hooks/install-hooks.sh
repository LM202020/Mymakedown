#!/usr/bin/env bash
set -euo pipefail
if [ ! -d ".git" ]; then
  echo "ERROR: .git directory not found. Run this from the repository root."
  exit 1
fi
mkdir -p .git/hooks
cp optional-hooks/git-hooks/pre-commit .git/hooks/pre-commit
cp optional-hooks/git-hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push
echo "Installed optional hooks."
