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
        "admin": {
            "password": hash_password("admin123"),
            "role": "administrator",
            "full_name": "Admin User",
            "department": "Administration",
            "email": "admin@district.gov"
        },
        "department1": {
            "password": hash_password("dept123"),
            "role": "department_head",
            "full_name": "Department Head 1",
            "department": "Public Works",
            "email": "dept1@district.gov"
        },
        "department2": {
            "password": hash_password("dept123"),
            "role": "department_head",
            "full_name": "Department Head 2",
            "department": "Health Services",
            "email": "dept2@district.gov"
        },
        "staff1": {
            "password": hash_password("staff123"),
            "role": "staff",
            "full_name": "Staff Member 1",
            "department": "Public Works",
            "email": "staff1@district.gov"
        },
        "staff2": {
            "password": hash_password("staff123"),
            "role": "staff",
            "full_name": "Staff Member 2",
            "department": "Health Services",
            "email": "staff2@district.gov"
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
