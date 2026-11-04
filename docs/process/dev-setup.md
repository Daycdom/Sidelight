# Developer Setup

| Field | Value |
| --- | --- |
| Status | Draft |
| Last updated | 2026-11-04 |

Windows is the main development machine, because the Screen Reader needs real Windows APIs (UI Automation, Windows Graphics Capture, Windows OCR). A Linux dev container is provided for cross-platform code only.

## Windows (recommended)

1. Install [winget](https://learn.microsoft.com/windows/package-manager/winget/) if it isn't present (it ships with Windows 11).
2. Clone the repo and run the setup script from the repo root:

   ```powershell
   git clone https://github.com/Daycdom/Sidelight.git sidelight
   cd sidelight
   powershell -ExecutionPolicy Bypass -File scripts\setup-windows.ps1
   ```

   It installs Git, uv, VS Code and Node.js if missing, installs Python 3.12 through uv, creates `.venv`, installs every package in editable mode, enables pre-commit hooks, and runs lint, type check and tests.
3. Open the folder in VS Code (`code .`) and accept the recommended extensions.

## WSL (git and cross-platform code)

WSL gives a Linux shell on Windows with fast git and the same tools as CI. From an Ubuntu WSL terminal:

```bash
bash setup-wsl.sh Daycdom/Sidelight   # script is in scripts/ of this repo
```

It installs git, the GitHub CLI and uv, signs you in to GitHub, clones the repo to `~/code/sidelight`, installs everything and runs the tests. Open it with `code .` (VS Code's WSL extension).

**Automatic sync:** the repo's VS Code settings fetch every 3 minutes and run "sync" (pull, then push) after every commit, so committing in VS Code keeps GitHub and your machine in step. Git is set to rebase on pull, so your history stays linear.

**Limit:** Python inside WSL is Linux Python. It cannot call Windows UI Automation, Windows Graphics Capture or Windows OCR. Do Screen Reader platform work and run `windows`-marked tests from the Windows setup above using a **second clone on the Windows side** (for example `C:\Users\<you>\source\repos\sidelight`). Don't run Windows `uv sync` inside the WSL folder: both would share one `.venv` and overwrite each other's Linux and Windows environments.

## macOS and Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
uv run pre-commit install
uv run pytest
```

Platform tests marked `windows` are skipped outside Windows.

## Dev container

Open the repo in VS Code and choose "Reopen in Container", or start a GitHub Codespace. Good for Redactor, Router and Copilot logic; not for Screen Reader platform work.

## Everyday commands

| Task | Command |
| --- | --- |
| Install or update dependencies | `uv sync` |
| Add a dependency to a package | `uv add --package sidelight-redact <name>` |
| Run all tests | `uv run pytest` |
| Run one package's tests | `uv run pytest packages/redact` |
| Lint and format | `uv run ruff check --fix` and `uv run ruff format` |
| Type check | `uv run mypy` |
| Run a CLI | `uv run sidelight-reader --help` |

## Package map

| Folder | Package (PyPI) | Import name | CLI |
| --- | --- | --- | --- |
| `packages/common` | `sidelight-common` | `sidelight_common` | `sidelight-common` |
| `packages/reader` | `sidelight-reader` | `sidelight_reader` | `sidelight-reader` |
| `packages/redact` | `sidelight-redact` | `sidelight_redact` | `sidelight-redact` |
| `packages/router` | `sidelight-router` | `sidelight_router` | `sidelight-router` |
| `packages/voice` | `sidelight-voice` | `sidelight_voice` | `sidelight-voice` |
| `packages/copilot` | `sidelight-copilot` | `sidelight_copilot` | `sidelight` |
