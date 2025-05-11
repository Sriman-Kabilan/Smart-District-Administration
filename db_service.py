import streamlit as st
from models import get_db_session, User, Task, TaskComment, ActivityLog, DepartmentPerformance, ResourceAllocation
import uuid
import hashlib
from datetime import datetime, timedelta
from sqlalchemy import desc, and_
import pandas as pd

# Function to hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to initialize database with sample data (if needed)
def initialize_database():
    db = get_db_session()
    
    # Check if users already exist
    if db.query(User).count() == 0:
        # Create sample users
        create_sample_users(db)
    
    # Check if department performance metrics exist
    if db.query(DepartmentPerformance).count() == 0:
        # Create sample performance data
        create_sample_performance_data(db)
    
    # Check if resource allocations exist
    if db.query(ResourceAllocation).count() == 0:
        # Create sample resource allocations
        create_sample_resource_allocations(db)
    
    db.close()

# Function to create sample users
def create_sample_users(db):
    # Administrator
    admin = User(
        username="admin",
        password=hash_password("admin123"),
        full_name="Admin User",
        email="admin@district.gov",
        role="administrator",
        department="Administration"
    )
    
    # Department Heads
    public_works_head = User(
        username="public_works_head",
        password=hash_password("dept123"),
        full_name="James Wilson",
        email="james.wilson@district.gov",
        role="department_head",
        department="Public Works"
    )
    
    health_head = User(
        username="health_head",
        password=hash_password("dept123"),
        full_name="Sarah Johnson",
        email="sarah.johnson@district.gov",
        role="department_head",
        department="Health Services"
    )
    
    education_head = User(
        username="education_head",
        password=hash_password("dept123"),
        full_name="Michael Brown",
        email="michael.brown@district.gov",
        role="department_head",
        department="Education"
    )
    
    transportation_head = User(
        username="transportation_head",
        password=hash_password("dept123"),
        full_name="Emily Davis",
        email="emily.davis@district.gov",
        role="department_head",
        department="Transportation"
    )
    
    security_head = User(
        username="security_head",
        password=hash_password("dept123"),
        full_name="Robert Johnson",
        email="robert.johnson@district.gov",
        role="department_head",
        department="Security"
    )
    
    # Staff members
    pw_staff1 = User(
        username="pw_staff1",
        password=hash_password("staff123"),
        full_name="John Smith",
        email="john.smith@district.gov",
        role="staff",
        department="Public Works"
    )
    
    pw_staff2 = User(
        username="pw_staff2",
        password=hash_password("staff123"),
        full_name="Maria Garcia",
        email="maria.garcia@district.gov",
        role="staff",
        department="Public Works"
    )
    
    pw_staff3 = User(
        username="pw_staff3",
        password=hash_password("staff123"),
        full_name="Lisa Wong",
        email="lisa.wong@district.gov",
        role="staff",
        department="Public Works"
    )
    
    health_staff1 = User(
        username="health_staff1",
        password=hash_password("staff123"),
        full_name="David Lee",
        email="david.lee@district.gov",
        role="staff",
        department="Health Services"
    )
    
    health_staff2 = User(
        username="health_staff2",
        password=hash_password("staff123"),
        full_name="Jessica Williams",
        email="jessica.williams@district.gov",
        role="staff",
        department="Health Services"
    )
    
    health_staff3 = User(
        username="health_staff3",
        password=hash_password("staff123"),
        full_name="Michael Brown",
        email="michael.brown.health@district.gov",
        role="staff",
        department="Health Services"
    )
    
    edu_staff1 = User(
        username="edu_staff1",
        password=hash_password("staff123"),
        full_name="Thomas Moore",
        email="thomas.moore@district.gov",
        role="staff",
        department="Education"
    )
    
    edu_staff2 = User(
        username="edu_staff2",
        password=hash_password("staff123"),
        full_name="Jennifer Martin",
        email="jennifer.martin@district.gov",
        role="staff",
        department="Education"
    )
    
    trans_staff1 = User(
        username="trans_staff1",
        password=hash_password("staff123"),
        full_name="Daniel Rodriguez",
        email="daniel.rodriguez@district.gov",
        role="staff",
        department="Transportation"
    )
    
    trans_staff2 = User(
        username="trans_staff2",
        password=hash_password("staff123"),
        full_name="Amanda Clark",
        email="amanda.clark@district.gov",
        role="staff",
        department="Transportation"
    )
    
    security_staff1 = User(
        username="security_staff1",
        password=hash_password("staff123"),
        full_name="Richard Harris",
        email="richard.harris@district.gov",
        role="staff",
        department="Security"
    )
    
    security_staff2 = User(
        username="security_staff2",
        password=hash_password("staff123"),
        full_name="Patricia Martinez",
        email="patricia.martinez@district.gov",
        role="staff",
        department="Security"
    )
    
    # Add all users to the database
    users = [
        admin, 
        public_works_head, health_head, education_head, transportation_head, security_head,
        pw_staff1, pw_staff2, pw_staff3,
        health_staff1, health_staff2, health_staff3,
        edu_staff1, edu_staff2,
        trans_staff1, trans_staff2,
        security_staff1, security_staff2
    ]
    
    for user in users:
        db.add(user)
    
    db.commit()

# Function to create sample performance data
def create_sample_performance_data(db):
    departments = ["Public Works", "Health Services", "Education", "Transportation", "Security"]
    today = datetime.now().date()
    
    # Create data for the past 30 days
    for i in range(30):
        date = today - timedelta(days=i)
        
        for department in departments:
            # Randomize metrics but keep them somewhat reasonable
            import random
            
            # Make efficiency_score vary between 65 and 95
            efficiency_score = 75 + random.randint(-10, 20)
            
            # Make task_completion_rate vary between 60 and 100
            task_completion_rate = 80 + random.randint(-20, 20)
            
            # Make budget_utilization vary between 70 and 95
            budget_utilization = 85 + random.randint(-15, 10)
            
            # Make citizen_satisfaction vary between 70 and 90
            citizen_satisfaction = 80 + random.randint(-10, 10)
            
            # Create the performance record
            performance = DepartmentPerformance(
                department=department,
                date=date,
                efficiency_score=efficiency_score,
                task_completion_rate=task_completion_rate,
                budget_utilization=budget_utilization,
                citizen_satisfaction=citizen_satisfaction
            )
            
            db.add(performance)
    
    db.commit()

# Function to create sample resource allocations
def create_sample_resource_allocations(db):
    departments = ["Public Works", "Health Services", "Education", "Transportation", "Security"]
    current_year = datetime.now().year
    
    # Budget allocations for each department (in thousands)
    budget_allocations = {
        "Public Works": 1200,
        "Health Services": 1500,
        "Education": 2000,
        "Transportation": 1000,
        "Security": 800
    }
    
    # Staff allocations for each department
    staff_allocations = {
        "Public Works": 50,
        "Health Services": 80,
        "Education": 100,
        "Transportation": 40,
        "Security": 30
    }
    
    # Equipment allocations for each department (in thousands)
    equipment_allocations = {
        "Public Works": 500,
        "Health Services": 700,
        "Education": 300,
        "Transportation": 800,
        "Security": 400
    }
    
    # Create allocations for the current year, all 12 months
    for month in range(1, 13):
        for department in departments:
            # Add some variations to monthly allocations
            import random
            
            # Vary monthly budget between 90% and 110% of the average
            budget_variation = random.uniform(0.9, 1.1)
            monthly_budget = budget_allocations[department] / 12 * budget_variation
            
            # Vary monthly staff slightly
            staff_variation = random.uniform(0.95, 1.05)
            monthly_staff = int(staff_allocations[department] * staff_variation)
            
            # Vary monthly equipment allocation
            equip_variation = random.uniform(0.85, 1.15)
            monthly_equipment = equipment_allocations[department] / 12 * equip_variation
            
            # Create the resource allocation record
            allocation = ResourceAllocation(
                department=department,
                year=current_year,
                month=month,
                budget_allocation=monthly_budget,
                staff_allocation=monthly_staff,
                equipment_allocation=monthly_equipment
            )
            
            db.add(allocation)
    
    db.commit()

# User Authentication Functions

def authenticate_user_db(username, password):
    db = get_db_session()
    hashed_password = hash_password(password)
    
    user = db.query(User).filter(User.username == username).first()
    
    if user and user.password == hashed_password:
        # Log successful login
        log_activity_db(username, "login", "successful")
        db.close()
        return True, user.role, user.id
    
    # Log failed login attempt
    if username:
        log_activity_db(username, "login", "failed")
    
    db.close()
    return False, None, None

def register_user_db(username, password, full_name, email, role, department):
    """
    Register a new user in the database.
    
    Parameters:
    - username: Unique username for the new user
    - password: Password for the new user (will be hashed)
    - full_name: Full name of the user
    - email: Email address of the user
    - role: User role (administrator, department_head, staff)
    - department: Department name the user belongs to
    
    Returns:
    - Tuple of (success, message, user_id)
      - success: Boolean indicating if registration was successful
      - message: Message describing the result
      - user_id: UUID of the new user if successful, None otherwise
    """
    db = get_db_session()
    
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        db.close()
        return False, "Username already exists", None
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        db.close()
        return False, "Email already exists", None
    
    # Hash the password
    hashed_password = hash_password(password)
    
    # Create new user
    new_user = User(
        username=username,
        password=hashed_password,
        full_name=full_name,
        email=email,
        role=role,
        department=department
    )
    
    try:
        db.add(new_user)
        db.commit()
        
        # Log the registration
        log_activity_db(username, "registration", "successful", f"Registered as {role} in {department}")
        
        user_id = new_user.id
        db.close()
        return True, "User registered successfully", user_id
    except Exception as e:
        db.rollback()
        db.close()
        return False, f"Registration failed: {str(e)}", None

def get_user_by_username(username):
    db = get_db_session()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user

def get_user_by_id(user_id):
    db = get_db_session()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    return user

def get_users_by_role(role):
    db = get_db_session()
    users = db.query(User).filter(User.role == role).all()
    result = []
    
    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "department": user.department,
            "email": user.email,
            "created_at": user.created_at.strftime("%Y-%m-%d") if user.created_at else "N/A"
        })
    
    db.close()
    return result

def get_all_users():
    """
    Get all users in the system, sorted by role and department.
    
    Returns:
    - List of user dictionaries
    """
    db = get_db_session()
    users = db.query(User).order_by(User.role, User.department, User.username).all()
    result = []
    
    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role,
            "department": user.department,
            "email": user.email,
            "created_at": user.created_at.strftime("%Y-%m-%d") if user.created_at else "N/A"
        })
    
    db.close()
    return result

def update_user_db(user_id, data):
    """
    Update a user in the database.
    
    Parameters:
    - user_id: UUID of user to update
    - data: Dictionary containing fields to update, which can include:
        - full_name: New full name
        - email: New email
        - role: New role
        - department: New department
        - password: New password (will be hashed)
    
    Returns:
    - Tuple of (success, message)
    """
    db = get_db_session()
    
    # Try to find the user
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        db.close()
        return False, "User not found"
    
    # Update fields if provided
    if "full_name" in data:
        user.full_name = data["full_name"]
    
    if "email" in data and data["email"] != user.email:
        # Check if email is unique
        existing_email = db.query(User).filter(User.email == data["email"], User.id != user_id).first()
        if existing_email:
            db.close()
            return False, "Email already in use by another user"
        user.email = data["email"]
    
    if "role" in data:
        user.role = data["role"]
    
    if "department" in data:
        user.department = data["department"]
    
    if "password" in data and data["password"]:
        user.password = hash_password(data["password"])
    
    try:
        user.updated_at = datetime.now()
        db.commit()
        db.close()
        return True, "User updated successfully"
    except Exception as e:
        db.rollback()
        db.close()
        return False, f"Error updating user: {str(e)}"

def delete_user_db(user_id, deleted_by_username):
    """
    Delete a user from the database.
    
    Parameters:
    - user_id: UUID of user to delete
    - deleted_by_username: Username of the admin performing the deletion
    
    Returns:
    - Tuple of (success, message)
    """
    db = get_db_session()
    
    # Try to find the user
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        db.close()
        return False, "User not found"
    
    # Don't allow deleting the last administrator
    if user.role == "administrator":
        admin_count = db.query(User).filter(User.role == "administrator").count()
        if admin_count <= 1:
            db.close()
            return False, "Cannot delete the last administrator account"
    
    # Store username for logging
    username = user.username
    
    try:
        # Delete user
        db.delete(user)
        db.commit()
        
        # Log the deletion
        log_activity_db(
            deleted_by_username, 
            f"deleted user {username}", 
            "successful",
            f"Deleted user with ID {user_id}"
        )
        
        db.close()
        return True, f"User {username} deleted successfully"
    except Exception as e:
        db.rollback()
        db.close()
        return False, f"Error deleting user: {str(e)}"

def get_users_by_department(department):
    db = get_db_session()
    users = db.query(User).filter(User.department == department).all()
    result = []
    
    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role,
            "email": user.email
        })
    
    db.close()
    return result

def get_staff_by_department(department):
    db = get_db_session()
    users = db.query(User).filter(
        User.department == department,
        User.role == "staff"
    ).all()
    
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email
        })
    
    db.close()
    return result

# Task Management Functions

def create_task_db(task_name, description, assigned_to_id, priority, due_date, created_by_id, department):
    db = get_db_session()
    
    # Generate a task ID for display (e.g., T-12345)
    task_id = f"T-{str(uuid.uuid4())[:5].upper()}"
    
    # Convert due_date string to date object if needed
    if isinstance(due_date, str):
        due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
    
    # Create the new task
    new_task = Task(
        task_id=task_id,
        task_name=task_name,
        description=description,
        assigned_to_id=assigned_to_id,
        created_by_id=created_by_id,
        priority=priority,
        status="Pending",
        department=department,
        due_date=due_date
    )
    
    db.add(new_task)
    
    # Get user information for logging
    created_by = db.query(User).filter(User.id == created_by_id).first()
    
    # Log the task creation
    if created_by:
        log_activity_db(created_by.username, f"created task {task_id}", "successful")
    
    db.commit()
    db.close()
    
    return task_id

def get_tasks_db(department=None, assigned_to_id=None, created_by_id=None, status=None, priority=None):
    db = get_db_session()
    
    # Start with a base query
    query = db.query(Task)
    
    # Apply filters
    if department:
        query = query.filter(Task.department == department)
    
    if assigned_to_id:
        query = query.filter(Task.assigned_to_id == assigned_to_id)
    
    if created_by_id:
        query = query.filter(Task.created_by_id == created_by_id)
    
    if status:
        query = query.filter(Task.status == status)
    
    if priority:
        query = query.filter(Task.priority == priority)
    
    # Execute the query
    tasks = query.all()
    
    # Prepare results
    results = []
    for task in tasks:
        # Get creator and assignee names
        creator = db.query(User).filter(User.id == task.created_by_id).first()
        assignee = db.query(User).filter(User.id == task.assigned_to_id).first()
        
        task_dict = {
            "id": task.id,
            "task_id": task.task_id,
            "task_name": task.task_name,
            "description": task.description,
            "created_by": creator.full_name if creator else "Unknown",
            "created_by_id": task.created_by_id,
            "assigned_to": assignee.full_name if assignee else "Unassigned",
            "assigned_to_id": task.assigned_to_id,
            "priority": task.priority,
            "status": task.status,
            "department": task.department,
            "created_date": task.created_at.strftime("%Y-%m-%d"),
            "due_date": task.due_date.strftime("%Y-%m-%d") if task.due_date else None,
            "completed_date": task.completed_date.strftime("%Y-%m-%d") if task.completed_date else None,
            "comments": []
        }
        
        # Get comments for this task
        comments = db.query(TaskComment).filter(TaskComment.task_id == task.id).order_by(TaskComment.timestamp).all()
        
        for comment in comments:
            commenter = db.query(User).filter(User.id == comment.user_id).first()
            task_dict["comments"].append({
                "text": comment.text,
                "by": commenter.full_name if commenter else "Unknown",
                "timestamp": comment.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        results.append(task_dict)
    
    db.close()
    return results

def get_task_by_id_db(task_id):
    db = get_db_session()
    
    # Try to find by UUID first
    try:
        uuid_id = uuid.UUID(task_id)
        task = db.query(Task).filter(Task.id == uuid_id).first()
    except ValueError:
        # If not a valid UUID, try to find by task_id string
        task = db.query(Task).filter(Task.task_id == task_id).first()
    
    if not task:
        db.close()
        return None
    
    # Get creator and assignee names
    creator = db.query(User).filter(User.id == task.created_by_id).first()
    assignee = db.query(User).filter(User.id == task.assigned_to_id).first()
    
    task_dict = {
        "id": task.id,
        "task_id": task.task_id,
        "task_name": task.task_name,
        "description": task.description,
        "created_by": creator.full_name if creator else "Unknown",
        "created_by_id": task.created_by_id,
        "assigned_to": assignee.full_name if assignee else "Unassigned",
        "assigned_to_id": task.assigned_to_id,
        "priority": task.priority,
        "status": task.status,
        "department": task.department,
        "created_date": task.created_at.strftime("%Y-%m-%d"),
        "due_date": task.due_date.strftime("%Y-%m-%d") if task.due_date else None,
        "completed_date": task.completed_date.strftime("%Y-%m-%d") if task.completed_date else None,
        "comments": []
    }
    
    # Get comments for this task
    comments = db.query(TaskComment).filter(TaskComment.task_id == task.id).order_by(TaskComment.timestamp).all()
    
    for comment in comments:
        commenter = db.query(User).filter(User.id == comment.user_id).first()
        task_dict["comments"].append({
            "text": comment.text,
            "by": commenter.full_name if commenter else "Unknown",
            "timestamp": comment.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    db.close()
    return task_dict

def update_task_status_db(task_id, new_status, updated_by_username):
    db = get_db_session()
    
    # Try to find by UUID first
    try:
        uuid_id = uuid.UUID(task_id)
        task = db.query(Task).filter(Task.id == uuid_id).first()
    except ValueError:
        # If not a valid UUID, try to find by task_id string
        task = db.query(Task).filter(Task.task_id == task_id).first()
    
    if not task:
        db.close()
        return False
    
    # Update the task status
    task.status = new_status
    
    # If completed, set completed date
    current_date = datetime.now().date()
    if new_status == "Completed":
        # Convert date to string then back to date to avoid SQLAlchemy type issues
        task.completed_date = current_date
    else:
        # Use NULL for completed_date
        task.completed_date = None
    
    # Log the activity
    log_activity_db(updated_by_username, f"updated task {task.task_id} status to {new_status}", "successful")
    
    db.commit()
    db.close()
    
    return True

def add_task_comment_db(task_id, comment_text, comment_by_username):
    db = get_db_session()
    
    # Get the user ID from the username
    user = db.query(User).filter(User.username == comment_by_username).first()
    
    if not user:
        db.close()
        return False
    
    # Try to find task by UUID first
    try:
        uuid_id = uuid.UUID(task_id)
        task = db.query(Task).filter(Task.id == uuid_id).first()
    except ValueError:
        # If not a valid UUID, try to find by task_id string
        task = db.query(Task).filter(Task.task_id == task_id).first()
    
    if not task:
        db.close()
        return False
    
    # Create the comment
    comment = TaskComment(
        text=comment_text,
        task_id=task.id,
        user_id=user.id
    )
    
    db.add(comment)
    
    # Log the activity
    log_activity_db(comment_by_username, f"commented on task {task.task_id}", "successful")
    
    db.commit()
    db.close()
    
    return True

# Activity Logging Function

def log_activity_db(username, action, status, details=None):
    db = get_db_session()
    
    log_entry = ActivityLog(
        username=username,
        action=action,
        status=status,
        details=details
    )
    
    db.add(log_entry)
    db.commit()
    db.close()

# Performance Data Functions

def get_department_data_db(department=None):
    db = get_db_session()
    
    # Start with a base query
    query = db.query(DepartmentPerformance)
    
    # Apply department filter if provided
    if department:
        query = query.filter(DepartmentPerformance.department == department)
    
    # Get the last 30 days of data
    today = datetime.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    query = query.filter(DepartmentPerformance.date >= thirty_days_ago)
    
    # Sort by date
    query = query.order_by(DepartmentPerformance.date)
    
    # Execute the query
    performance_data = query.all()
    
    # Convert to DataFrame for easier manipulation
    data_list = []
    for data in performance_data:
        data_list.append({
            "date": data.date,
            "department": data.department,
            "efficiency_score": data.efficiency_score,
            "task_completion_rate": data.task_completion_rate,
            "budget_utilization": data.budget_utilization,
            "citizen_satisfaction": data.citizen_satisfaction,
            # Add week and month columns for aggregation
            "week": data.date.isocalendar()[1],  # ISO week number
            "month": data.date.month
        })
    
    df = pd.DataFrame(data_list)
    
    db.close()
    return df

def get_performance_data_db(department=None, all_departments=False, by_staff=False):
    db = get_db_session()
    
    # If by_staff is True, we need to calculate performance metrics for each staff member
    if by_staff:
        # Get all staff members in the department
        staff_members = db.query(User).filter(
            User.department == department,
            User.role == "staff"
        ).all()
        
        results = []
        for staff in staff_members:
            # Count total tasks
            total_tasks = db.query(Task).filter(
                Task.assigned_to_id == staff.id,
                Task.department == department
            ).count()
            
            # Count completed tasks
            completed_tasks = db.query(Task).filter(
                Task.assigned_to_id == staff.id,
                Task.department == department,
                Task.status == "Completed"
            ).count()
            
            # Calculate efficiency score (completed / total * 100)
            efficiency_score = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            # Check on-time completion rate
            on_time_tasks = db.query(Task).filter(
                Task.assigned_to_id == staff.id,
                Task.department == department,
                Task.status == "Completed",
                Task.completed_date <= Task.due_date
            ).count()
            
            on_time_rate = (on_time_tasks / completed_tasks * 100) if completed_tasks > 0 else 0
            
            results.append({
                "staff_name": staff.full_name,
                "tasks_completed": completed_tasks,
                "total_tasks": total_tasks,
                "efficiency_score": efficiency_score,
                "on_time_rate": on_time_rate
            })
        
        db.close()
        return pd.DataFrame(results)
    
    # Handle regular performance data request
    else:
        # Start with a base query
        query = db.query(DepartmentPerformance)
        
        # Apply filters
        if department and not all_departments:
            query = query.filter(DepartmentPerformance.department == department)
        
        # Get the data for the last 6 months
        today = datetime.now().date()
        six_months_ago = today - timedelta(days=180)
        
        query = query.filter(DepartmentPerformance.date >= six_months_ago)
        
        # Execute the query
        performance_data = query.all()
        
        # Process into the required format
        results = []
        for data in performance_data:
            month_name = data.date.strftime("%b")
            
            results.append({
                "department": data.department,
                "date": data.date,
                "month": month_name,
                "efficiency_score": data.efficiency_score,
                "task_completion_rate": data.task_completion_rate,
                "budget_utilization": data.budget_utilization,
                "citizen_satisfaction": data.citizen_satisfaction
            })
        
        db.close()
        return pd.DataFrame(results)

def get_resource_data_db(department=None, all_departments=False):
    db = get_db_session()
    
    # Start with a base query
    query = db.query(ResourceAllocation)
    
    # Apply filters
    if department and not all_departments:
        query = query.filter(ResourceAllocation.department == department)
    
    # Get the current year's data
    current_year = datetime.now().year
    query = query.filter(ResourceAllocation.year == current_year)
    
    # Execute the query
    allocations = query.all()
    
    # Process into the required format
    results = []
    for allocation in allocations:
        results.append({
            "department": allocation.department,
            "month": allocation.month,
            "budget_allocation": allocation.budget_allocation,
            "staff_allocation": allocation.staff_allocation,
            "equipment_allocation": allocation.equipment_allocation
        })
    
    db.close()
    return pd.DataFrame(results)

def get_activity_logs(limit=15):
    db = get_db_session()
    
    # Get the most recent activity logs
    logs = db.query(ActivityLog).order_by(desc(ActivityLog.timestamp)).limit(limit).all()
    
    # Process into a list of dictionaries
    results = []
    for log in logs:
        results.append({
            "username": log.username,
            "action": log.action,
            "status": log.status,
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "details": log.details
        })
    
    db.close()
    return results