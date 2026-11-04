#!/usr/bin/env bash
# Sidelight: one-time developer setup inside WSL (Ubuntu).
# Usage (from a WSL terminal):
#   curl -fsSL <raw URL of this file> | bash -s -- <owner>/<repo>
# or, after cloning:  bash scripts/setup-wsl.sh <owner>/<repo>
set -euo pipefail

REPO="${1:?Pass the GitHub repo, e.g. yourname/sidelight}"
DEST="${HOME}/code/$(basename "$REPO")"

echo "... installing git, curl and GitHub CLI"
sudo apt-get update -y
sudo apt-get install -y git curl gh

echo "... installing uv"
if ! command -v uv >/dev/null; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

if [ -z "$(git config --global user.name || true)" ]; then
  read -rp "Git name: " name;   git config --global user.name "$name"
  read -rp "Git email: " email; git config --global user.email "$email"
fi
git config --global pull.rebase true
git config --global rebase.autoStash true
git config --global push.autoSetupRemote true
git config --global init.defaultBranch main

echo "... signing in to GitHub (opens a browser code flow)"
gh auth status >/dev/null 2>&1 || gh auth login --git-protocol https --web
gh auth setup-git

if [ ! -d "$DEST/.git" ]; then
  mkdir -p "$(dirname "$DEST")"
  gh repo clone "$REPO" "$DEST"
fi
cd "$DEST"

echo "... installing packages"
uv sync
uv run pre-commit install
uv run pytest -q

echo
echo "Done. Open it in VS Code from WSL:  cd $DEST && code ."
echo "Commits made in VS Code now pull and push automatically (git.postCommitCommand = sync)."
