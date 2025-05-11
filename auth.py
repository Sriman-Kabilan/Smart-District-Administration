import streamlit as st
import hashlib
from datetime import datetime
from db_service import (
    initialize_database, authenticate_user_db, get_user_by_username, register_user_db,
    get_users_by_role as get_users_by_role_db,
    get_users_by_department as get_users_by_department_db,
    get_staff_by_department as get_staff_by_department_db,
    log_activity_db
)

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to create initial user data
def create_user_data():
    # Initialize the database with sample data
    initialize_database()

# Function to authenticate users
def authenticate_user(username, password):
    # Use database authentication
    authenticated, role, user_id = authenticate_user_db(username, password)
    
    if authenticated:
        # Store user_id in session state for later use
        st.session_state.user_id = user_id
        return True, role
    
    return False, None

# Function to register a new user
def register_user(username, password, full_name, email, role, department):
    """
    Register a new user with the given details.
    
    Parameters:
    - username: Unique username for the new user
    - password: Password for the new user
    - full_name: Full name of the user
    - email: Email address of the user
    - role: User role (administrator, department_head, staff)
    - department: Department name the user belongs to
    
    Returns:
    - Tuple of (success, message, user_id)
    """
    # Use database registration service
    return register_user_db(username, password, full_name, email, role, department)

# Function to get all users by role
def get_users_by_role(role):
    return get_users_by_role_db(role)

# Function to get all users in a specific department
def get_users_by_department(department):
    return get_users_by_department_db(department)

# Function to get staff members of a department
def get_staff_by_department(department):
    return get_staff_by_department_db(department)

# Function to check if a user is authenticated
def check_user_auth():
    return st.session_state.authenticated

# Function to get the department of the current user
def get_user_department():
    if "username" in st.session_state:
        user = get_user_by_username(st.session_state.username)
        if user:
            return user.department
    return None

# Function to get the full name of the current user
def get_user_fullname():
    if "username" in st.session_state:
        user = get_user_by_username(st.session_state.username)
        if user:
            return user.full_name
    return None

# Function to log user activity
def log_activity(username, action, status):
    # Log to database
    log_activity_db(username, action, status)
    
    # Also keep in-memory logs for the current session
    if "activity_log" not in st.session_state:
        st.session_state.activity_log = []
    
    log_entry = {
        "username": username,
        "action": action,
        "status": status,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    st.session_state.activity_log.append(log_entry)