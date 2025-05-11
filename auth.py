import streamlit as st
import json
import hashlib
import os
from datetime import datetime

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to create initial user data
def create_user_data():
    # Users data structure with role-based access
    users = {
        # Administrator Account
        "admin": {
            "password": hash_password("admin123"),
            "role": "administrator",
            "full_name": "Admin User",
            "department": "Administration",
            "email": "admin@district.gov"
        },
        
        # Department Heads
        "public_works_head": {
            "password": hash_password("dept123"),
            "role": "department_head",
            "full_name": "James Wilson",
            "department": "Public Works",
            "email": "james.wilson@district.gov"
        },
        "health_head": {
            "password": hash_password("dept123"),
            "role": "department_head",
            "full_name": "Sarah Johnson",
            "department": "Health Services",
            "email": "sarah.johnson@district.gov"
        },
        "education_head": {
            "password": hash_password("dept123"),
            "role": "department_head",
            "full_name": "Michael Brown",
            "department": "Education",
            "email": "michael.brown@district.gov"
        },
        "transportation_head": {
            "password": hash_password("dept123"),
            "role": "department_head",
            "full_name": "Emily Davis",
            "department": "Transportation",
            "email": "emily.davis@district.gov"
        },
        "security_head": {
            "password": hash_password("dept123"),
            "role": "department_head",
            "full_name": "Robert Johnson",
            "department": "Security",
            "email": "robert.johnson@district.gov"
        },
        
        # Public Works Staff
        "pw_staff1": {
            "password": hash_password("staff123"),
            "role": "staff",
            "full_name": "John Smith",
            "department": "Public Works",
            "email": "john.smith@district.gov"
        },
        "pw_staff2": {
            "password": hash_password("staff123"),
            "role": "staff",
            "full_name": "Maria Garcia",
            "department": "Public Works",
            "email": "maria.garcia@district.gov"
        },
        "pw_staff3": {
            "password": hash_password("staff123"),
            "role": "staff",
            "full_name": "Lisa Wong",
            "department": "Public Works",
            "email": "lisa.wong@district.gov"
        },
        
        # Health Services Staff
        "health_staff1": {
            "password": hash_password("staff123"),
            "role": "staff",
            "full_name": "David Lee",
            "department": "Health Services",
            "email": "david.lee@district.gov"
        },
        "health_staff2": {
            "password": hash_password("staff123"),
            "role": "staff",
            "full_name": "Jessica Williams",
            "department": "Health Services",
            "email": "jessica.williams@district.gov"
        },
        "health_staff3": {
            "password": hash_password("staff123"),
            "role": "staff",
            "full_name": "Michael Brown",
            "department": "Health Services",
            "email": "michael.brown.health@district.gov"
        },
        
        # Education Staff
        "edu_staff1": {
            "password": hash_password("staff123"),
            "role": "staff",
            "full_name": "Thomas Moore",
            "department": "Education",
            "email": "thomas.moore@district.gov"
        },
        "edu_staff2": {
            "password": hash_password("staff123"),
            "role": "staff",
            "full_name": "Jennifer Martin",
            "department": "Education",
            "email": "jennifer.martin@district.gov"
        },
        
        # Transportation Staff
        "trans_staff1": {
            "password": hash_password("staff123"),
            "role": "staff",
            "full_name": "Daniel Rodriguez",
            "department": "Transportation",
            "email": "daniel.rodriguez@district.gov"
        },
        "trans_staff2": {
            "password": hash_password("staff123"),
            "role": "staff",
            "full_name": "Amanda Clark",
            "department": "Transportation",
            "email": "amanda.clark@district.gov"
        },
        "trans_staff3": {
            "password": hash_password("staff123"),
            "role": "staff",
            "full_name": "William Taylor",
            "department": "Transportation",
            "email": "william.taylor@district.gov"
        },
        
        # Security Staff
        "security_staff1": {
            "password": hash_password("staff123"),
            "role": "staff",
            "full_name": "Richard Harris",
            "department": "Security",
            "email": "richard.harris@district.gov"
        },
        "security_staff2": {
            "password": hash_password("staff123"),
            "role": "staff",
            "full_name": "Patricia Martinez",
            "department": "Security",
            "email": "patricia.martinez@district.gov"
        }
    }
    
    # Store the user data in session state for this demo
    st.session_state.users = users

# Function to authenticate users
def authenticate_user(username, password):
    # Get users from session state
    users = st.session_state.users
    
    # Check if username exists
    if username in users:
        # Check if password matches
        if users[username]["password"] == hash_password(password):
            # Log successful login
            log_activity(username, "login", "successful")
            return True, users[username]["role"]
    
    # Log failed login attempt
    if username:
        log_activity(username, "login", "failed")
    
    return False, None

# Function to get all users by role
def get_users_by_role(role):
    users_list = []
    for username, user_data in st.session_state.users.items():
        if user_data["role"] == role:
            users_list.append({
                "username": username,
                "full_name": user_data["full_name"],
                "department": user_data["department"],
                "email": user_data["email"]
            })
    return users_list

# Function to get all users in a specific department
def get_users_by_department(department):
    users_list = []
    for username, user_data in st.session_state.users.items():
        if user_data["department"] == department:
            users_list.append({
                "username": username,
                "full_name": user_data["full_name"],
                "role": user_data["role"],
                "email": user_data["email"]
            })
    return users_list

# Function to get staff members of a department
def get_staff_by_department(department):
    users_list = []
    for username, user_data in st.session_state.users.items():
        if user_data["department"] == department and user_data["role"] == "staff":
            users_list.append({
                "username": username,
                "full_name": user_data["full_name"],
                "email": user_data["email"]
            })
    return users_list

# Function to check if a user is authenticated
def check_user_auth():
    return st.session_state.authenticated

# Function to get user department
def get_user_department():
    if st.session_state.authenticated and st.session_state.username:
        return st.session_state.users[st.session_state.username]["department"]
    return None

# Function to get user full name
def get_user_fullname():
    if st.session_state.authenticated and st.session_state.username:
        return st.session_state.users[st.session_state.username]["full_name"]
    return None

# Function to log user activity
def log_activity(username, action, status):
    # Initialize activity log if not exists
    if "activity_log" not in st.session_state:
        st.session_state.activity_log = []
    
    # Add new activity
    st.session_state.activity_log.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username": username,
        "action": action,
        "status": status
    })
