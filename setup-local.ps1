# PowerShell script for setting up District Administration Dashboard for local development

Write-Host "Setting up District Administration Dashboard for local development..." -ForegroundColor Green

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Write-Host "Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "Node.js is not installed. Please install Node.js first." -ForegroundColor Red
    Write-Host "Download from: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    try {
        $pythonVersion = python3 --version
        Write-Host "Python found: $pythonVersion" -ForegroundColor Green
        $pythonCmd = "python3"
        $pipCmd = "pip3"
    } catch {
        Write-Host "Python 3 is not installed. Please install Python 3 first." -ForegroundColor Red
        Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
        exit 1
    }
}

if (-not $pythonCmd) {
    $pythonCmd = "python"
    $pipCmd = "pip"
}

# Install frontend dependencies
Write-Host "Installing frontend dependencies..." -ForegroundColor Blue
npm install

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install frontend dependencies" -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Blue
    Copy-Item ".env.example" ".env"
    Write-Host "Please edit .env file with your database credentials" -ForegroundColor Yellow
} else {
    Write-Host ".env file already exists" -ForegroundColor Green
}

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Blue
$packages = @(
    "fastapi",
    "uvicorn[standard]",
    "sqlalchemy",
    "psycopg2-binary",
    "pydantic",
    "python-jose[cryptography]",
    "passlib[bcrypt]",
    "python-multipart",
    "pandas",
    "numpy",
    "scikit-learn",
    "plotly",
    "altair"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..." -ForegroundColor Cyan
    & $pipCmd install $package
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install $package" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To run the application:" -ForegroundColor Yellow
Write-Host "1. Start backend: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload" -ForegroundColor White
Write-Host "2. Start frontend: npm start" -ForegroundColor White
Write-Host ""
Write-Host "Make sure to:" -ForegroundColor Yellow
Write-Host "- Set up your PostgreSQL database" -ForegroundColor White
Write-Host "- Update the DATABASE_URL in .env file" -ForegroundColor White
Write-Host "- Create the database: createdb district_admin" -ForegroundColor White
Write-Host ""
Write-Host "Demo accounts:" -ForegroundColor Cyan
Write-Host "- Administrator: admin / admin123" -ForegroundColor White
Write-Host "- Department Head: dept_head / dept123" -ForegroundColor White
Write-Host "- Staff Member: staff / staff123" -ForegroundColor White