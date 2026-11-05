# Sidelight: one-time Windows developer setup.
# Run in PowerShell from the repo root:  powershell -ExecutionPolicy Bypass -File scripts\setup-windows.ps1
$ErrorActionPreference = "Stop"

function Install-IfMissing($command, $wingetId) {
    if (Get-Command $command -ErrorAction SilentlyContinue) {
        Write-Host "OK  $command already installed"
    } else {
        Write-Host "... installing $wingetId"
        winget install --id $wingetId --exact --silent --accept-package-agreements --accept-source-agreements
    }
}

Install-IfMissing git    "Git.Git"
Install-IfMissing uv     "astral-sh.uv"
Install-IfMissing code   "Microsoft.VisualStudioCode"
Install-IfMissing node   "OpenJS.NodeJS.LTS"   # needed from phase 6 (desktop UI)

# Refresh PATH for this session so newly installed tools are found.
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
            [System.Environment]::GetEnvironmentVariable("Path", "User")

Write-Host "... installing Python 3.12 (managed by uv)"
uv python install 3.12

Write-Host "... creating .venv and installing all packages"
uv sync

Write-Host "... enabling pre-commit hooks"
uv run pre-commit install

Write-Host "... running checks"
uv run ruff check
uv run mypy
uv run pytest

Write-Host ""
Write-Host "Done. Open the folder in VS Code:  code ."
