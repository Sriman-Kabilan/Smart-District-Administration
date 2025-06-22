# Windows Setup Guide

## Quick Installation

### Method 1: PowerShell (Recommended)
1. Open PowerShell as Administrator
2. Navigate to the project directory
3. Run the setup script:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   .\setup-local.ps1
   ```

### Method 2: Command Prompt
1. Open Command Prompt as Administrator
2. Navigate to the project directory
3. Run:
   ```cmd
   setup-local.bat
   ```

## Prerequisites Installation

### Install Node.js
1. Download from [nodejs.org](https://nodejs.org/)
2. Choose the LTS version
3. Run the installer with default settings
4. Verify installation: `node --version`

### Install Python
1. Download from [python.org](https://www.python.org/downloads/)
2. **Important**: Check "Add Python to PATH" during installation
3. Verify installation: `python --version`

### Install PostgreSQL
1. Download from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Remember the password you set for the postgres user
3. Add PostgreSQL to your PATH if not done automatically

## Database Setup
```cmd
# Create database
createdb -U postgres district_admin

# Or using psql
psql -U postgres
CREATE DATABASE district_admin;
\q
```

## Environment Configuration
1. Copy `.env.example` to `.env`
2. Update the DATABASE_URL:
   ```
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/district_admin
   ```

## Running the Application

### Start Backend
```cmd
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### Start Frontend (New Terminal)
```cmd
npm start
```

## Common Issues

### Python not found
- Reinstall Python and ensure "Add to PATH" is checked
- Or manually add Python to your system PATH

### PostgreSQL connection issues
- Ensure PostgreSQL service is running
- Check username/password in .env file
- Verify database exists: `psql -U postgres -l`

### Port conflicts
- Backend: Change port with `--port 8001`
- Frontend: Set `PORT=3001` before running `npm start`

## Demo Accounts
- Administrator: `admin` / `admin123`
- Department Head: `dept_head` / `dept123`
- Staff Member: `staff` / `staff123`