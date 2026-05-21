#!/usr/bin/env bash
set -euo pipefail
rm -f .git/hooks/pre-commit
rm -f .git/hooks/pre-push
echo "Removed optional hooks."
