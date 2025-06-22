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
        "http://localhost:5000",  # Replit/custom port
        "https://*.replit.dev",   # Replit domains
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