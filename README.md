# Smart District Administration Dashboard

Please refer to the comprehensive [PROJECT_OVERVIEW.md](file:///s:/Smart-District-Administration/PROJECT_OVERVIEW.md) for full details on project architecture, technologies, operational modules, running instructions, and demo credentials.

## Quick Start

### 1. Start Backend API
```powershell
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
Endpoint: `http://localhost:8000` (API Docs: `http://localhost:8000/docs`)

### 2. Start Frontend UI
```powershell
npm start
```
Endpoint: `http://localhost:3000`

### Demo Credentials
- **Administrator**: `admin` / `admin123`
- **Department Head**: `dept_head` / `dept123`
- **Staff Member**: `staff` / `staff123`

