# Local Development Setup Guide

## Prerequisites
- Node.js (version 14 or higher)
- Python 3.8 or higher
- PostgreSQL database

## Quick Setup

### Windows Users
Run one of these automated setup scripts:
```powershell
# PowerShell (recommended)
.\setup-local.ps1

# Or Command Prompt
setup-local.bat
```

### Linux/Mac Users
```bash
./setup-local.sh
```

## Manual Setup

### 1. Backend Setup
```bash
# Install Python dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-jose passlib python-multipart pandas numpy scikit-learn plotly altair

# Set up environment variables
export DATABASE_URL="postgresql://username:password@localhost:5432/district_admin"
```

### 2. Frontend Setup
```bash
# Install Node.js dependencies
npm install

# Create .env file in root directory with:
REACT_APP_API_URL=http://localhost:8000
```

### 3. Database Setup
```bash
# Create PostgreSQL database
createdb district_admin

# The application will automatically create tables on first run
```

## Running the Application

### Start Backend (Terminal 1)
```bash
# From project root
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### Start Frontend (Terminal 2)
```bash
# From project root
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Demo Accounts
- Administrator: admin / admin123
- Department Head: dept_head / dept123
- Staff Member: staff / staff123

## Troubleshooting

### CORS Issues
If you encounter CORS errors, ensure the backend CORS configuration includes your local frontend URL.

### Database Connection
Make sure your DATABASE_URL is correctly configured and the PostgreSQL service is running.

### Port Conflicts
If ports 3000 or 8000 are in use, you can change them:
- Frontend: Set PORT=3001 before running npm start
- Backend: Change --port parameter in uvicorn command

## Production Deployment
For production deployment, build the React app and serve it with a proper web server:
```bash
npm run build
# Serve the build folder with nginx, apache, or similar
```