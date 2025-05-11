import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from auth import get_user_department, get_user_fullname, get_staff_by_department, log_activity
from db_service import (
    create_task_db, get_tasks_db, update_task_status_db, 
    add_task_comment_db, get_task_by_id_db
)

# Initialize session state for tasks if not exists
def initialize_task_data():
    # No need to initialize anything since we're using the database
    pass

# Function to create a new task
def create_task(task_name, description, assigned_to, priority, due_date, created_by, department):
    # Get the assigned user's ID
    staff_list = get_staff_by_department(department)
    assigned_to_id = None
    
    for staff in staff_list:
        if staff["full_name"] == assigned_to:
            assigned_to_id = staff["id"]
            break
    
    if assigned_to_id is None:
        st.error(f"Could not find user {assigned_to}")
        return None
    
    # Get creator's user_id from session state
    created_by_id = st.session_state.user_id
    
    # Create the task in the database
    task_id = create_task_db(
        task_name=task_name,
        description=description,
        assigned_to_id=assigned_to_id,
        priority=priority,
        due_date=due_date,
        created_by_id=created_by_id,
        department=department
    )
    
    return task_id

# Function to get tasks filtered by parameters
def get_tasks(department=None, assigned_to=None, created_by=None, status=None, priority=None):
    # Convert full names to IDs if provided
    assigned_to_id = None
    created_by_id = None
    
    # Use the database service to get tasks
    return get_tasks_db(
        department=department,
        assigned_to_id=assigned_to_id,
        created_by_id=created_by_id,
        status=status,
        priority=priority
    )

# Function to update task status
def update_task_status(task_id, new_status, updated_by):
    # Use database service
    return update_task_status_db(task_id, new_status, updated_by)

# Function to add a comment to a task
def add_task_comment(task_id, comment_text, comment_by):
    # Use database service
    return add_task_comment_db(task_id, comment_text, comment_by)

# Function to get task by ID
def get_task_by_id(task_id):
    # Use database service
    return get_task_by_id_db(task_id)

# Function to display task creation form for department heads
def display_task_creation_form():
    department = get_user_department()
    created_by = get_user_fullname()
    username = st.session_state.username
    
    with st.form("create_task_form"):
        st.subheader("Create New Task")
        
        task_name = st.text_input("Task Name")
        description = st.text_area("Task Description")
        
        # Get staff members in the department for assignment
        staff_list = get_staff_by_department(department)
        staff_names = [staff["full_name"] for staff in staff_list]
        
        assigned_to = st.selectbox("Assign To", staff_names)
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        due_date = st.date_input("Due Date", datetime.now() + timedelta(days=7))
        
        submitted = st.form_submit_button("Create Task")
        
        if submitted:
            if not task_name:
                st.error("Task name is required")
            elif not description:
                st.error("Task description is required")
            else:
                task_id = create_task(
                    task_name=task_name,
                    description=description,
                    assigned_to=assigned_to,
                    priority=priority,
                    due_date=due_date.strftime("%Y-%m-%d"),
                    created_by=created_by,
                    department=department
                )
                
                if task_id:
                    st.success(f"Task created successfully with ID: {task_id}")
                    return True
                else:
                    st.error("Failed to create task")
    
    return False

# Function to display task list with filtering options
def display_task_list():
    st.subheader("Task Management")
    
    # Get user info
    department = get_user_department()
    full_name = get_user_fullname()
    role = st.session_state.user_role
    
    # Filtering options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox(
            "Filter by Status", 
            ["All", "Pending", "In Progress", "Completed", "Canceled"]
        )
    
    with col2:
        priority_filter = st.selectbox(
            "Filter by Priority",
            ["All", "Low", "Medium", "High", "Critical"]
        )
    
    with col3:
        if role == "department_head":
            view_type = st.selectbox(
                "View Tasks",
                ["All Department Tasks", "Created by Me", "Specific Staff Member"]
            )
        else:
            view_type = "Assigned to Me"
    
    # Apply filters
    if status_filter != "All":
        status = status_filter
    else:
        status = None
        
    if priority_filter != "All":
        priority = priority_filter
    else:
        priority = None
    
    # Get tasks based on role and view selection
    if role == "department_head":
        if view_type == "All Department Tasks":
            filtered_tasks = get_tasks(department=department, status=status, priority=priority)
        elif view_type == "Created by Me":
            filtered_tasks = get_tasks(department=department, created_by=full_name, status=status, priority=priority)
        else:
            # If viewing for specific staff member
            staff_list = get_staff_by_department(department)
            staff_names = [staff["full_name"] for staff in staff_list]
            selected_staff = st.selectbox("Select Staff Member", staff_names)
            filtered_tasks = get_tasks(department=department, assigned_to=selected_staff, status=status, priority=priority)
    else:
        # Staff members can only see tasks assigned to them
        filtered_tasks = get_tasks(department=department, assigned_to=full_name, status=status, priority=priority)
    
    # Display tasks
    if not filtered_tasks:
        st.info("No tasks found matching the selected filters.")
    else:
        # Sort tasks by priority and due date
        sorted_tasks = sorted(
            filtered_tasks, 
            key=lambda x: (
                ["Critical", "High", "Medium", "Low"].index(x["priority"]),
                x["due_date"]
            )
        )
        
        # Display each task as an expander
        for task in sorted_tasks:
            # Determine task status color
            if task["status"] == "Completed":
                status_color = "green"
            elif task["status"] == "In Progress":
                status_color = "blue"
            elif task["status"] == "Canceled":
                status_color = "gray"
            elif task["priority"] == "Critical":
                status_color = "red"
            elif task["priority"] == "High":
                status_color = "orange"
            else:
                status_color = "black"
            
            # Create expander label with color
            expander_label = f"{task['task_id']} - {task['task_name']} - {task['priority']} Priority - :{status_color}[{task['status']}]"
            
            with st.expander(expander_label):
                # Task details
                st.markdown(f"**Description:** {task['description']}")
                st.markdown(f"**Assigned to:** {task['assigned_to']}")
                st.markdown(f"**Created by:** {task['created_by']}")
                st.markdown(f"**Department:** {task['department']}")
                st.markdown(f"**Due Date:** {task['due_date']}")
                st.markdown(f"**Created Date:** {task['created_date']}")
                
                if task['completed_date']:
                    st.markdown(f"**Completed Date:** {task['completed_date']}")
                
                # Task actions
                if task["status"] != "Completed" and task["status"] != "Canceled":
                    # Status update options
                    if role == "department_head" or task["assigned_to"] == full_name:
                        new_status = st.selectbox(
                            "Update Status:",
                            ["Pending", "In Progress", "Completed", "Canceled"],
                            ["Pending", "In Progress", "Completed", "Canceled"].index(task["status"]),
                            key=f"status_{task['task_id']}"
                        )
                        
                        if st.button("Update Status", key=f"update_{task['task_id']}"):
                            if update_task_status(task["task_id"], new_status, st.session_state.username):
                                st.success(f"Task status updated to {new_status}")
                                st.rerun()
                            else:
                                st.error("Failed to update task status")
                
                # Comments section
                st.markdown("---")
                st.markdown("### Comments")
                
                if "comments" in task and task["comments"]:
                    for comment in task["comments"]:
                        st.markdown(f"**{comment['by']}** ({comment['timestamp']}): {comment['text']}")
                else:
                    st.info("No comments yet")
                
                # Add comment
                new_comment = st.text_area("Add Comment", key=f"comment_{task['task_id']}")
                if st.button("Submit Comment", key=f"submit_comment_{task['task_id']}"):
                    if new_comment:
                        if add_task_comment(task["task_id"], new_comment, st.session_state.username):
                            st.success("Comment added successfully")
                            st.rerun()
                        else:
                            st.error("Failed to add comment")
                    else:
                        st.warning("Please enter a comment")

# Function to display task dashboard with statistics
def display_task_dashboard():
    department = get_user_department()
    full_name = get_user_fullname()
    role = st.session_state.user_role
    
    st.subheader("Task Dashboard")
    
    # Get tasks based on role
    if role == "department_head":
        department_tasks = get_tasks(department=department)
    else:
        department_tasks = get_tasks(department=department, assigned_to=full_name)
    
    # Calculate statistics
    total_tasks = len(department_tasks)
    pending_tasks = len([task for task in department_tasks if task["status"] == "Pending"])
    in_progress_tasks = len([task for task in department_tasks if task["status"] == "In Progress"])
    completed_tasks = len([task for task in department_tasks if task["status"] == "Completed"])
    canceled_tasks = len([task for task in department_tasks if task["status"] == "Canceled"])
    
    # Calculate overdue tasks
    today = datetime.now().strftime("%Y-%m-%d")
    overdue_tasks = len([
        task for task in department_tasks 
        if task["due_date"] < today and task["status"] not in ["Completed", "Canceled"]
    ])
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tasks", total_tasks)
    
    with col2:
        st.metric("Pending", pending_tasks)
    
    with col3:
        st.metric("In Progress", in_progress_tasks)
    
    with col4:
        st.metric("Completed", completed_tasks)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Overdue Tasks", overdue_tasks, delta=None, delta_color="inverse")
    
    with col2:
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    # Display recent tasks
    st.subheader("Recent Tasks")
    
    # Sort tasks by created date in descending order
    sorted_tasks = sorted(department_tasks, key=lambda x: x["created_date"], reverse=True)
    recent_tasks = sorted_tasks[:5] if len(sorted_tasks) > 5 else sorted_tasks
    
    if recent_tasks:
        for task in recent_tasks:
            st.markdown(
                f"**{task['task_id']}** - {task['task_name']} - **Status:** {task['status']} - "
                f"**Due:** {task['due_date']} - **Assigned to:** {task['assigned_to']}"
            )
    else:
        st.info("No tasks found")