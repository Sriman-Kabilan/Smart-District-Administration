@echo off
echo Setting up District Administration Dashboard for local development...

:: Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js is not installed. Please install Node.js first.
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Python 3 is not installed. Please install Python 3 first.
        echo Download from: https://www.python.org/downloads/
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=python3
        set PIP_CMD=pip3
    )
) else (
    set PYTHON_CMD=python
    set PIP_CMD=pip
)

:: Install frontend dependencies
echo Installing frontend dependencies...
npm install
if %errorlevel% neq 0 (
    echo Failed to install frontend dependencies
    pause
    exit /b 1
)

:: Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy ".env.example" ".env"
    echo Please edit .env file with your database credentials
) else (
    echo .env file already exists
)

:: Install Python dependencies
echo Installing Python dependencies...
%PIP_CMD% install fastapi uvicorn[standard] sqlalchemy psycopg2-binary pydantic python-jose[cryptography] passlib[bcrypt] python-multipart pandas numpy scikit-learn plotly altair

echo.
echo Setup complete!
echo.
echo To run the application:
echo 1. Start backend: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
echo 2. Start frontend: npm start
echo.
echo Make sure to:
echo - Set up your PostgreSQL database
echo - Update the DATABASE_URL in .env file
echo - Create the database: createdb district_admin
echo.
echo Demo accounts:
echo - Administrator: admin / admin123
echo - Department Head: dept_head / dept123
echo - Staff Member: staff / staff123
echo.
pause