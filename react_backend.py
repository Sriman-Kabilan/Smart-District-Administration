# FastAPI Backend - main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
import bcrypt
import os
from typing import Optional, List
import uvicorn

# Database imports
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Date, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Pydantic models for request/response
from pydantic import BaseModel, EmailStr
from typing import Union

# Initialize FastAPI app
app = FastAPI(title="District Administration API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/dbname")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Security
security = HTTPBearer()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    role = Column(String)  # administrator, department_head, staff
    department = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    created_tasks = relationship("Task", foreign_keys="Task.created_by_id", back_populates="creator")
    assigned_tasks = relationship("Task", foreign_keys="Task.assigned_to_id", back_populates="assignee")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(String, unique=True, index=True)
    task_name = Column(String)
    description = Column(Text)
    priority = Column(String)  # Low, Medium, High, Critical
    status = Column(String, default="Pending")  # Pending, In Progress, Completed, Canceled
    department = Column(String)
    due_date = Column(Date)
    completed_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    assigned_to_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    creator = relationship("User", foreign_keys=[created_by_id], back_populates="created_tasks")
    assignee = relationship("User", foreign_keys=[assigned_to_id], back_populates="assigned_tasks")
    comments = relationship("TaskComment", back_populates="task")

class TaskComment(Base):
    __tablename__ = "task_comments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    task = relationship("Task", back_populates="comments")
    user = relationship("User")

class DepartmentPerformance(Base):
    __tablename__ = "department_performance"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    department = Column(String)
    date = Column(Date)
    efficiency_score = Column(Float)
    task_completion_rate = Column(Float)
    budget_utilization = Column(Float)
    citizen_satisfaction = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class ResourceAllocation(Base):
    __tablename__ = "resource_allocations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    department = Column(String)
    year = Column(Integer)
    month = Column(Integer)
    budget_allocation = Column(Float)
    staff_allocation = Column(Integer)
    equipment_allocation = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic Models
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: str
    department: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    department: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    task_name: str
    description: str
    priority: str
    department: str
    due_date: str
    assigned_to: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    task_name: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[str] = None

class TaskResponse(TaskBase):
    id: str
    task_id: str
    status: str
    created_at: datetime
    creator: UserResponse
    assignee: UserResponse
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Utility Functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

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

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Authentication Routes
@app.post("/auth/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )

@app.post("/auth/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role=user_data.role,
        department=user_data.department
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse.from_orm(db_user)

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return UserResponse.from_orm(current_user)

@app.get("/auth/users", response_model=List[UserResponse])
async def get_all_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role not in ["administrator", "department_head"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    if current_user.role == "administrator":
        users = db.query(User).all()
    else:
        users = db.query(User).filter(User.department == current_user.department).all()
    
    return [UserResponse.from_orm(user) for user in users]

# Task Routes
@app.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(
    department: Optional[str] = None,
    assigned_to: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Task)
    
    # Apply role-based filtering
    if current_user.role == "staff":
        query = query.filter(Task.assigned_to_id == current_user.id)
    elif current_user.role == "department_head":
        query = query.filter(Task.department == current_user.department)
    
    # Apply additional filters
    if department:
        query = query.filter(Task.department == department)
    if assigned_to:
        assignee = db.query(User).filter(User.username == assigned_to).first()
        if assignee:
            query = query.filter(Task.assigned_to_id == assignee.id)
    if status:
        query = query.filter(Task.status == status)
    
    tasks = query.all()
    return [TaskResponse.from_orm(task) for task in tasks]

@app.post("/tasks", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "staff":
        raise HTTPException(status_code=403, detail="Staff cannot create tasks")
    
    # Find assignee
    assignee = db.query(User).filter(User.username == task_data.assigned_to).first()
    if not assignee:
        raise HTTPException(status_code=404, detail="Assignee not found")
    
    # Generate task ID
    task_count = db.query(Task).count()
    task_id = f"T-{task_count + 1:06d}"
    
    # Create task
    db_task = Task(
        task_id=task_id,
        task_name=task_data.task_name,
        description=task_data.description,
        priority=task_data.priority,
        department=task_data.department,
        due_date=datetime.strptime(task_data.due_date, "%Y-%m-%d").date(),
        created_by_id=current_user.id,
        assigned_to_id=assignee.id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return TaskResponse.from_orm(db_task)

@app.patch("/tasks/{task_id}/status")
async def update_task_status(
    task_id: str,
    status: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check permissions
    if current_user.role == "staff" and task.assigned_to_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    task.status = status["status"]
    if status["status"] == "Completed":
        task.completed_date = datetime.utcnow().date()
    
    db.commit()
    return {"message": "Task status updated successfully"}

# Dashboard Routes
@app.get("/dashboard/overview")
async def get_dashboard_overview(
    department: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "staff":
        # Staff dashboard data
        my_tasks = db.query(Task).filter(Task.assigned_to_id == current_user.id).all()
        completed_week = db.query(Task).filter(
            Task.assigned_to_id == current_user.id,
            Task.status == "Completed",
            Task.completed_date >= datetime.utcnow().date() - timedelta(days=7)
        ).count()
        
        return {
            "my_tasks": len(my_tasks),
            "completed_week": completed_week,
            "pending_tasks": len([t for t in my_tasks if t.status == "Pending"])
        }
    
    elif current_user.role == "department_head":
        # Department head dashboard data
        dept_tasks = db.query(Task).filter(Task.department == current_user.department).all()
        completed_tasks = [t for t in dept_tasks if t.status == "Completed"]
        team_members = db.query(User).filter(
            User.department == current_user.department,
            User.role == "staff"
        ).count()
        
        completion_rate = (len(completed_tasks) / len(dept_tasks) * 100) if dept_tasks else 0
        
        return {
            "department_tasks": len(dept_tasks),
            "completion_rate": completion_rate,
            "team_members": team_members,
            "efficiency_score": 85.5  # This would be calculated from performance metrics
        }
    
    else:
        # Administrator dashboard data
        total_tasks = db.query(Task).count()
        departments = db.query(User.department).distinct().count()
        total_staff = db.query(User).filter(User.role == "staff").count()
        
        return {
            "total_departments": departments,
            "active_tasks": total_tasks,
            "total_staff": total_staff,
            "budget_utilization": 78.3  # This would come from resource allocation data
        }

# Analytics Routes
@app.get("/analytics/predictions")
async def get_predictions(
    department: str,
    periods: int = 3,
    model_type: str = "random_forest",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "staff":
        raise HTTPException(status_code=403, detail="Access denied")
    
    # This would typically use the machine learning models
    # For now, returning mock prediction structure
    predictions = []
    base_budget = 100000
    base_staff = 15
    
    for i in range(periods):
        month_ahead = datetime.utcnow() + timedelta(days=30 * (i + 1))
        predictions.append({
            "date": month_ahead.strftime("%Y-%m-%d"),
            "budget_allocation": base_budget * (1 + 0.05 * i),  # 5% growth
            "staff_allocation": base_staff + i,
            "equipment_allocation": base_budget * 0.2 * (1 + 0.03 * i)
        })
    
    return {
        "department": department,
        "model_type": model_type,
        "predictions": predictions,
        "confidence": 0.85
    }

@app.get("/analytics/optimization/{department}")
async def get_optimization_analysis(
    department: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "staff":
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Mock optimization data - would be calculated from actual performance metrics
    return {
        "current": {
            "budget": 100000,
            "staff": 15,
            "equipment": 20000
        },
        "recommended": {
            "budget": 105000,
            "staff": 16,
            "equipment": 21000
        },
        "change": {
            "budget": 5000,
            "budget_percent": 5.0,
            "staff": 1,
            "equipment": 1000,
            "equipment_percent": 5.0
        },
        "explanation": "Analysis suggests increasing budget allocation by 5% to improve performance metrics."
    }

if __name__ == "__main__":
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000)