<#
run_local.ps1

Helper script to set up and run the Financial Planner app on Windows (PowerShell).
Usage: Open PowerShell, navigate to the project folder, then run:
    .\run_local.ps1

What it does:
  - Ensures ExecutionPolicy for the current process allows running the venv activation script
  - Creates a virtual environment in `.venv` (if missing)
  - Activates the virtual environment
  - Installs Python dependencies from requirements.txt
  - Ensures a `.env` file exists (creates a placeholder if missing)
  - Starts the Flask development server

Notes:
  - This script sets ExecutionPolicy only for the current PowerShell process; it will not change system policies permanently.
  - You still should open the `.env` file and replace OPENAI_API_KEY with your real key before using the chatbot.
#>

Write-Host "== Financial Planner: Local dev helper ==" -ForegroundColor Cyan

# Make sure we're in the script directory
Set-Location -Path $PSScriptRoot

# Allow activation script in this process
Try {
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force | Out-Null
} Catch {
    Write-Warning "Could not set ExecutionPolicy for process. You may need to set it manually: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned"
}

# Check for python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not found on PATH. Please install Python 3.10+ and re-run this script."; exit 1
}

# Create venv if missing
if (-not (Test-Path -Path ".\.venv")) {
    Write-Host "Creating virtual environment .venv..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { Write-Error "Failed to create virtual environment"; exit 1 }
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

if (-not $env:VIRTUAL_ENV) {
    Write-Warning "Virtual environment may not have activated. You can activate manually with: .\\.venv\\Scripts\\Activate.ps1"
}

# Install dependencies
if (Test-Path -Path "requirements.txt") {
    Write-Host "Installing Python dependencies from requirements.txt..." -ForegroundColor Yellow
    pip install -r requirements.txt
} else {
    Write-Warning "requirements.txt not found. Skipping pip install.";
}

# Ensure .env exists
if (-not (Test-Path -Path ".env")) {
    Write-Warning ".env not found. Creating .env placeholder. Please add your OpenAI API key to .env before starting the server."
    "OPENAI_API_KEY=sk-REPLACE_ME" | Out-File -FilePath .env -Encoding utf8
    Write-Host "Created .env placeholder. Edit .env and add your real OPENAI_API_KEY." -ForegroundColor Yellow
}

# Start Flask app
Write-Host "Starting Flask development server..." -ForegroundColor Green
$env:FLASK_APP = "app.py"
$env:FLASK_DEBUG = "1"

# Run flask; this will block until server stops
flask run

# End
Write-Host "Flask server stopped." -ForegroundColor Cyan
