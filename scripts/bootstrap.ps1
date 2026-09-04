# Bootstrap script for ARIA QUANT
Write-Host "Bootstrapping ARIA QUANT environment..." -ForegroundColor Cyan

# Check if Python is installed
$python_cmd = "python"
if (!(Get-Command $python_cmd -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found. Please install Python 3.12." -ForegroundColor Red
    exit 1
}

$python_version = & $python_cmd --version 2>&1
Write-Host "Using Python version: $python_version"

# Create virtual environment if it doesn't exist
$venv_dir = ".env_aria"
if (!(Test-Path $venv_dir)) {
    Write-Host "Creating virtual environment in $venv_dir..."
    & $python_cmd -m venv $venv_dir
}

# Activate venv and install requirements
$activate_script = ".\$venv_dir\Scripts\Activate.ps1"
Write-Host "Installing dependencies..."
& cmd.exe /c ".\$venv_dir\Scripts\activate.bat && pip install --upgrade pip && pip install -r requirements.txt"

# Setup initial env file if missing
if (!(Test-Path "config\.env")) {
    Write-Host "Creating config\.env from example..."
    Copy-Item "config\.env.example" "config\.env"
}

Write-Host "Bootstrap complete! To activate the environment, run:" -ForegroundColor Green
Write-Host ".\$venv_dir\Scripts\Activate.ps1" -ForegroundColor Yellow
