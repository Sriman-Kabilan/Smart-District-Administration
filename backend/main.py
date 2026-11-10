from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import jwt
import bcrypt
import os
from datetime import datetime, timedelta

app = FastAPI(title="District Administration API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default port for local development
        "http://localhost:5000",  # Custom frontend port
        "*"  # Allow all origins as fallback
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "district-admin-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

# Pydantic Models
class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    full_name: str
    email: str
    role: str
    department: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TaskCreate(BaseModel):
    task_name: str
    description: Optional[str] = ""
    priority: str = "Medium"
    department: str
    assigned_to: str
    due_date: str

class TaskStatusUpdate(BaseModel):
    status: str

# Mock database
MOCK_USERS = {
    "admin": {
        "id": "1",
        "username": "admin",
        "password": bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        "full_name": "System Administrator",
        "email": "admin@district.gov",
        "role": "administrator",
        "department": "Administration"
    },
    "dept_head": {
        "id": "2",
        "username": "dept_head",
        "password": bcrypt.hashpw("dept123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        "full_name": "Department Head",
        "email": "head@district.gov",
        "role": "department_head",
        "department": "Public Works"
    },
    "staff": {
        "id": "3",
        "username": "staff",
        "password": bcrypt.hashpw("staff123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        "full_name": "Staff Member",
        "email": "staff@district.gov",
        "role": "staff",
        "department": "Public Works"
    }
}

MOCK_TASKS = [
    {
        "id": "1",
        "task_id": "T-001",
        "task_name": "Road Maintenance & Pothole Survey",
        "description": "Conduct comprehensive survey of arterial roads in Ward 2",
        "priority": "High",
        "status": "In Progress",
        "assigned_to": "staff",
        "due_date": "2026-11-20",
        "department": "Public Works"
    },
    {
        "id": "2",
        "task_id": "T-002",
        "task_name": "Quarterly Municipal Budget Analysis",
        "description": "Prepare expenditure reconciliation for Q3 audit",
        "priority": "Medium",
        "status": "Pending",
        "assigned_to": "dept_head",
        "due_date": "2026-11-25",
        "department": "Revenue & Finance"
    },
    {
        "id": "3",
        "task_id": "T-003",
        "task_name": "Primary School Water Quality Inspection",
        "description": "Sample testing across 12 civic schools",
        "priority": "Critical",
        "status": "Completed",
        "assigned_to": "staff",
        "due_date": "2026-11-10",
        "department": "Health & Sanitation"
    },
    {
        "id": "4",
        "task_id": "T-004",
        "task_name": "Traffic Signal Synchronization on Ring Road",
        "description": "Deploy firmware update to automated signal controllers",
        "priority": "High",
        "status": "In Progress",
        "assigned_to": "staff",
        "due_date": "2026-11-18",
        "department": "Transportation"
    }
]

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = MOCK_USERS.get(username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.post("/auth/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    user = MOCK_USERS.get(login_data.username)
    if not user or not verify_password(login_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    user_response = UserResponse(
        id=user["id"],
        username=user["username"],
        full_name=user["full_name"],
        email=user["email"],
        role=user["role"],
        department=user["department"]
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id=current_user["id"],
        username=current_user["username"],
        full_name=current_user["full_name"],
        email=current_user["email"],
        role=current_user["role"],
        department=current_user["department"]
    )

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None

@app.put("/auth/me", response_model=UserResponse)
async def update_current_user_info(update_data: UserUpdateRequest, current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    user = MOCK_USERS.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if update_data.full_name is not None:
        user["full_name"] = update_data.full_name
    if update_data.email is not None:
        user["email"] = update_data.email
    if update_data.department is not None:
        user["department"] = update_data.department
    return UserResponse(
        id=user["id"],
        username=user["username"],
        full_name=user["full_name"],
        email=user["email"],
        role=user["role"],
        department=user["department"]
    )

@app.get("/dashboard/overview")
async def get_dashboard_overview(current_user: dict = Depends(get_current_user)):
    if current_user["role"] == "staff":
        return {
            "my_tasks": 8,
            "completed_week": 5,
            "pending_tasks": 3
        }
    elif current_user["role"] == "department_head":
        return {
            "department_tasks": 24,
            "completion_rate": 87.5,
            "team_members": 12,
            "efficiency_score": 92.1,
            "task_change_percent": 8.3
        }
    else:
        return {
            "total_departments": 7,
            "active_tasks": 142,
            "total_staff": 89,
            "budget_utilization": 78.3,
            "task_change_percent": 12.5
        }

@app.get("/")
async def root():
    return {"message": "District Administration API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)