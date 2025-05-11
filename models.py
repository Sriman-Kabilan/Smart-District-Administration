import os
import uuid
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Table, Text, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import UUID

# Get the database URL from environment variables
DATABASE_URL = os.environ.get('DATABASE_URL')

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL if DATABASE_URL is not None else "")

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class for declarative models
Base = declarative_base()

# Function to get a database session
def get_db_session():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

# Define the User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)
    email = Column(String, unique=True)
    role = Column(String)  # administrator, department_head, staff
    department = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    tasks_created = relationship("Task", back_populates="creator", foreign_keys="Task.created_by_id")
    tasks_assigned = relationship("Task", back_populates="assignee", foreign_keys="Task.assigned_to_id")

# Define the Task model
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(String, unique=True, index=True)  # For display purposes, e.g., T-12345
    task_name = Column(String)
    description = Column(Text)
    priority = Column(String)  # Low, Medium, High, Critical
    status = Column(String, default="Pending")  # Pending, In Progress, Completed, Canceled
    department = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    due_date = Column(Date)
    completed_date = Column(Date, nullable=True)
    
    # Foreign keys
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    assigned_to_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    creator = relationship("User", back_populates="tasks_created", foreign_keys=[created_by_id])
    assignee = relationship("User", back_populates="tasks_assigned", foreign_keys=[assigned_to_id])
    comments = relationship("TaskComment", back_populates="task", cascade="all, delete-orphan")

# Define the Task Comment model
class TaskComment(Base):
    __tablename__ = "task_comments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(Text)
    timestamp = Column(DateTime, default=datetime.now)
    
    # Foreign keys
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    task = relationship("Task", back_populates="comments")
    user = relationship("User")

# Define the Department Performance model for storing metrics
class DepartmentPerformance(Base):
    __tablename__ = "department_performance"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    department = Column(String)
    date = Column(Date)  # For tracking historical data
    efficiency_score = Column(Float)
    task_completion_rate = Column(Float)
    budget_utilization = Column(Float)
    citizen_satisfaction = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Define the Resource Allocation model
class ResourceAllocation(Base):
    __tablename__ = "resource_allocations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    department = Column(String)
    year = Column(Integer)
    month = Column(Integer)
    budget_allocation = Column(Float)
    staff_allocation = Column(Integer)
    equipment_allocation = Column(Float)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Define the Activity Log model
class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String)
    action = Column(String)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.now)
    details = Column(Text, nullable=True)

# Create all tables in the database (if they don't exist)
Base.metadata.create_all(bind=engine)