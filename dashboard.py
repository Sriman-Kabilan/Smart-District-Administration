import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import uuid
from datetime import datetime, timedelta
from utils.data_handler import get_department_data, get_performance_data, get_resource_data, get_task_data
from utils.visualization import create_kpi_card, create_performance_chart, create_resource_chart
from utils.kpi_calculations import calculate_performance_metrics
from task_manager import initialize_task_data, display_task_creation_form, display_task_list, display_task_dashboard
from db_service import get_all_users, update_user_db, delete_user_db, register_user_db

# Admin Dashboard
def display_admin_dashboard():
    # Initialize task data
    initialize_task_data()
    
    st.title("District Administration Dashboard")
    st.write(f"Welcome, {st.session_state.username} (Administrator)")
    
    # Create tabs for different dashboard sections
    dashboard_tabs = st.tabs(["Overview", "Department Performance", "Resource Allocation", "Task Management", "User Management", "Activity Log"])
    
    # Overview Tab
    with dashboard_tabs[0]:
        # Overview metrics
        st.subheader("District Overview")
        
        # KPI metrics row
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        # Get actual task count from the task manager
        total_tasks = len(st.session_state.tasks) if "tasks" in st.session_state else 0
        open_tasks = len([t for t in st.session_state.tasks if t["status"] in ["Pending", "In Progress"]]) if "tasks" in st.session_state else 0
        
        with kpi1:
            create_kpi_card("Total Departments", "5", "10% ↑", "#1E88E5")
        
        with kpi2:
            create_kpi_card("Open Tasks", str(open_tasks), f"{5 if open_tasks > 20 else -5}% {'↑' if open_tasks > 20 else '↓'}", "#43A047")
        
        with kpi3:
            create_kpi_card("Resource Utilization", "78%", "3% ↑", "#FB8C00") 
        
        with kpi4:
            create_kpi_card("Citizen Satisfaction", "86%", "2% ↑", "#8E24AA")
    
    # Performance Metrics Tab
    with dashboard_tabs[1]:
        # Performance metrics section
        st.subheader("Department Performance")
        
        # Get performance data
        performance_data = get_performance_data(all_departments=True)
        
        # Create performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                performance_data, 
                x='department', 
                y='efficiency_score',
                color='efficiency_score',
                color_continuous_scale='Blues',
                title="Department Efficiency Scores"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig2 = px.line(
                performance_data, 
                x='month', 
                y='task_completion_rate', 
                color='department',
                title="Task Completion Rate by Department"
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
    
    # Resource Allocation Tab
    with dashboard_tabs[2]:
        # Resource allocation section
        st.subheader("Resource Allocation")
        
        # Get resource data
        resource_data = get_resource_data(all_departments=True)
        
        # Create resource allocation chart
        fig3 = px.pie(
            resource_data, 
            values='budget_allocation', 
            names='department',
            title="Budget Allocation by Department"
        )
        fig3.update_layout(height=500)
        st.plotly_chart(fig3, use_container_width=True)
    
    # Task Management Tab
    with dashboard_tabs[3]:
        st.subheader("Task Management System")
        st.write("Monitor and manage tasks across all departments")
        
        # Display task dashboard with statistics
        display_task_dashboard()
        
        # Display the task list interface
        display_task_list()
    
    # User Management Tab
    with dashboard_tabs[4]:
        st.subheader("User Management")
        st.write("Manage users and their access levels in the system")
        
        # Create tabs for different user management functions
        user_tabs = st.tabs(["All Users", "Create User", "Edit User", "Delete User"])
        
        # All Users Tab
        with user_tabs[0]:
            st.subheader("All System Users")
            
            # Get all users from the database
            all_users = get_all_users()
            
            if all_users:
                # Convert to DataFrame for better display
                users_df = pd.DataFrame(all_users)
                
                # Select columns to display
                display_columns = ["username", "full_name", "role", "department", "email", "created_at"]
                
                # Display users in a table
                st.dataframe(users_df[display_columns], use_container_width=True)
                
                # Show user counts by role
                role_counts = users_df['role'].value_counts().reset_index()
                role_counts.columns = ['Role', 'Count']
                
                # Display counts
                st.subheader("User Counts by Role")
                col1, col2 = st.columns([2, 3])
                
                with col1:
                    st.table(role_counts)
                
                with col2:
                    fig = px.pie(role_counts, values='Count', names='Role', title="User Distribution by Role")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No users found in the system.")
        
        # Create User Tab
        with user_tabs[1]:
            st.subheader("Create New User")
            
            with st.form("create_user_form"):
                # Personal information
                full_name = st.text_input("Full Name")
                username = st.text_input("Username")
                email = st.text_input("Email")
                
                # Role and department
                role = st.selectbox(
                    "Role", 
                    ["administrator", "department_head", "staff"]
                )
                
                department = st.selectbox(
                    "Department",
                    ["Administration", "Public Works", "Health Services", "Education", "Transportation", "Security"]
                )
                
                # Password
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                
                # Submit button
                submit_button = st.form_submit_button("Create User")
                
                if submit_button:
                    # Validate inputs
                    if not full_name or not username or not email or not password:
                        st.error("Please fill in all required fields")
                    elif password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        # Register the user
                        success, message, user_id = register_user_db(
                            username=username,
                            password=password,
                            full_name=full_name,
                            email=email,
                            role=role,
                            department=department
                        )
                        
                        if success:
                            st.success(f"User {username} created successfully!")
                        else:
                            st.error(f"Failed to create user: {message}")
        
        # Edit User Tab
        with user_tabs[2]:
            st.subheader("Edit Existing User")
            
            # Get all users
            all_users = get_all_users()
            
            if all_users:
                # Create a dictionary of users for the selectbox
                user_options = {f"{user['username']} ({user['full_name']})": user for user in all_users}
                
                # Select user to edit
                selected_user_display = st.selectbox(
                    "Select User to Edit",
                    options=list(user_options.keys())
                )
                
                if selected_user_display:
                    selected_user = user_options[selected_user_display]
                    
                    with st.form("edit_user_form"):
                        # Display current values and allow editing
                        user_id = selected_user["id"]
                        st.text_input("Username", value=selected_user["username"], disabled=True)
                        full_name = st.text_input("Full Name", value=selected_user["full_name"])
                        email = st.text_input("Email", value=selected_user["email"])
                        
                        # Role and department
                        role_options = ["administrator", "department_head", "staff"]
                        current_role_index = role_options.index(selected_user["role"]) if selected_user["role"] in role_options else 0
                        
                        role = st.selectbox(
                            "Role", 
                            options=role_options,
                            index=current_role_index
                        )
                        
                        department_options = ["Administration", "Public Works", "Health Services", "Education", "Transportation", "Security"]
                        current_dept_index = department_options.index(selected_user["department"]) if selected_user["department"] in department_options else 0
                        
                        department = st.selectbox(
                            "Department",
                            options=department_options,
                            index=current_dept_index
                        )
                        
                        # New password (optional)
                        st.markdown("**Leave password fields empty to keep current password**")
                        password = st.text_input("New Password (optional)", type="password")
                        confirm_password = st.text_input("Confirm New Password", type="password")
                        
                        # Submit button
                        submit_button = st.form_submit_button("Update User")
                        
                        if submit_button:
                            # Validate inputs
                            if not full_name or not email:
                                st.error("Full name and email are required")
                            elif password and password != confirm_password:
                                st.error("Passwords do not match")
                            else:
                                # Prepare update data
                                update_data = {
                                    "full_name": full_name,
                                    "email": email,
                                    "role": role,
                                    "department": department
                                }
                                
                                # Add password if provided
                                if password:
                                    update_data["password"] = password
                                
                                # Update the user
                                success, message = update_user_db(user_id, update_data)
                                
                                if success:
                                    st.success(f"User updated successfully!")
                                else:
                                    st.error(f"Failed to update user: {message}")
            else:
                st.info("No users found in the system.")
        
        # Delete User Tab
        with user_tabs[3]:
            st.subheader("Delete User")
            st.warning("⚠️ Warning: Deleting a user is permanent and cannot be undone.")
            
            # Get all users
            all_users = get_all_users()
            
            if all_users:
                # Create a dictionary of users for the selectbox, excluding current user
                current_username = st.session_state.username
                user_options = {
                    f"{user['username']} ({user['full_name']})": user 
                    for user in all_users 
                    if user['username'] != current_username
                }
                
                if not user_options:
                    st.info("No other users available to delete.")
                else:
                    # Select user to delete
                    selected_user_display = st.selectbox(
                        "Select User to Delete",
                        options=list(user_options.keys())
                    )
                    
                    if selected_user_display:
                        selected_user = user_options[selected_user_display]
                        
                        # Display user details
                        st.write(f"**Username:** {selected_user['username']}")
                        st.write(f"**Full Name:** {selected_user['full_name']}")
                        st.write(f"**Role:** {selected_user['role']}")
                        st.write(f"**Department:** {selected_user['department']}")
                        st.write(f"**Email:** {selected_user['email']}")
                        
                        # Confirmation
                        confirmation = st.text_input(
                            "Type the username to confirm deletion", 
                            placeholder=f"Type '{selected_user['username']}' to confirm"
                        )
                        
                        if st.button("Delete User"):
                            if confirmation == selected_user['username']:
                                success, message = delete_user_db(selected_user['id'], current_username)
                                
                                if success:
                                    st.success(message)
                                else:
                                    st.error(message)
                            else:
                                st.error("Username confirmation doesn't match. Deletion cancelled.")
            else:
                st.info("No users found in the system.")
        
    # Activity Log Tab
    with dashboard_tabs[5]:
        # Recent activity section
        st.subheader("Recent System Activity")
        
        if "activity_log" in st.session_state:
            activity_df = pd.DataFrame(st.session_state.activity_log[-15:])
            if not activity_df.empty:
                # Sort by timestamp in descending order
                activity_df['timestamp'] = pd.to_datetime(activity_df['timestamp'])
                activity_df = activity_df.sort_values(by='timestamp', ascending=False)
                
                st.dataframe(activity_df, use_container_width=True)
            else:
                st.info("No activity recorded yet")
        else:
            st.info("No activity recorded yet")

# Department Head Dashboard
def display_department_head_dashboard():
    from auth import get_user_department
    
    # Initialize task data
    initialize_task_data()
    
    department = get_user_department()
    
    st.title(f"{department} Department Dashboard")
    st.write(f"Welcome, {st.session_state.username} (Department Head)")
    
    # Create tabs for different dashboard sections
    dashboard_tabs = st.tabs(["Department Overview", "Performance Metrics", "Staff Management", "Task Management"])
    
    # Department Overview Tab
    with dashboard_tabs[0]:
        # Overview metrics for the department
        st.subheader("Department Overview")
        
        # Calculate department metrics
        performance_metrics = calculate_performance_metrics(department)
        
        # Get actual task count from the task manager
        department_tasks = [t for t in st.session_state.tasks if t["department"] == department] if "tasks" in st.session_state else []
        actual_open_tasks = len([t for t in department_tasks if t["status"] in ["Pending", "In Progress"]])
        
        # KPI metrics row
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        with kpi1:
            create_kpi_card("Staff Members", str(performance_metrics['staff_count']), "", "#1E88E5")
        
        with kpi2:
            create_kpi_card("Open Tasks", str(actual_open_tasks), f"{performance_metrics['task_trend']}% {'↑' if performance_metrics['task_trend'] > 0 else '↓'}", "#43A047")
        
        with kpi3:
            create_kpi_card("Budget Utilized", f"{performance_metrics['budget_utilization']}%", f"{performance_metrics['budget_trend']}% {'↑' if performance_metrics['budget_trend'] > 0 else '↓'}", "#FB8C00") 
        
        with kpi4:
            create_kpi_card("Performance Score", f"{performance_metrics['performance_score']}/100", f"{performance_metrics['performance_trend']}% {'↑' if performance_metrics['performance_trend'] > 0 else '↓'}", "#8E24AA")
        
    # Performance Metrics Tab
    with dashboard_tabs[1]:
        # Department specific performance
        st.subheader("Department Performance")
        
        # Get department data
        department_data = get_department_data(department)
        
        # Create performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            chart = create_performance_chart(department_data, "weekly")
            if chart is not None:
                st.altair_chart(chart, use_container_width=True)
        
        with col2:
            resource_chart = create_resource_chart(department_data)
            if resource_chart is not None:
                st.altair_chart(resource_chart, use_container_width=True)
    
    # Staff Management Tab
    with dashboard_tabs[2]:
        # Staff performance section
        st.subheader("Staff Performance")
        
        # Get staff data for the department
        staff_data = get_performance_data(department=department, by_staff=True)
        
        # Create staff performance chart
        fig = px.bar(
            staff_data, 
            x='staff_name', 
            y='tasks_completed',
            color='efficiency_score',
            color_continuous_scale='Blues',
            title="Staff Task Completion and Efficiency"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Task status by staff
        st.subheader("Task Distribution by Staff")
        
        # Get legacy task data for visualization
        legacy_task_data = get_task_data(department=department)
        
        # Add a new chart showing task distribution by staff member
        if not legacy_task_data.empty:
            staff_task_count = legacy_task_data.groupby(['assigned_to', 'status']).size().reset_index(name='count')
            
            fig2 = px.bar(
                staff_task_count,
                x='assigned_to',
                y='count',
                color='status',
                title="Task Distribution by Staff Member",
                color_discrete_map={
                    'Pending': '#FFC107',
                    'In Progress': '#2196F3',
                    'Completed': '#4CAF50'
                }
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    # Task Management Tab
    with dashboard_tabs[3]:
        st.subheader("Task Management")
        
        # Create subtabs for creating and managing tasks
        task_tabs = st.tabs(["Create New Task", "Task Dashboard", "Manage Tasks"])
        
        with task_tabs[0]:
            # Display task creation form
            display_task_creation_form()
            
        with task_tabs[1]:
            # Display task dashboard with statistics
            display_task_dashboard()
            
        with task_tabs[2]:
            # Display the task list interface
            display_task_list()

# Staff Dashboard
def display_staff_dashboard():
    from auth import get_user_department, get_user_fullname
    
    # Initialize task data
    initialize_task_data()
    
    department = get_user_department()
    full_name = get_user_fullname()
    
    st.title("Staff Dashboard")
    st.write(f"Welcome, {full_name} ({department})")
    
    # Create tabs for different dashboard sections
    dashboard_tabs = st.tabs(["Task Overview", "Manage My Tasks", "My Performance"])
    
    # Task Overview Tab
    with dashboard_tabs[0]:
        st.subheader("My Task Overview")
        
        # Get assigned tasks from the real task manager
        my_tasks = [t for t in st.session_state.tasks if t["assigned_to"] == full_name] if "tasks" in st.session_state else []
        
        # Task counts from real data
        total_tasks = len(my_tasks)
        completed_tasks = len([t for t in my_tasks if t["status"] == "Completed"])
        in_progress_tasks = len([t for t in my_tasks if t["status"] == "In Progress"])
        pending_tasks = len([t for t in my_tasks if t["status"] == "Pending"])
        
        # Calculate completion rate
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Task KPI metrics row
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        with kpi1:
            create_kpi_card("Total Tasks", str(total_tasks), "", "#1E88E5")
            
        with kpi2:
            create_kpi_card("Pending Tasks", str(pending_tasks), "", "#FB8C00")
        
        with kpi3:
            create_kpi_card("In Progress", str(in_progress_tasks), "", "#1E88E5")
        
        with kpi4:
            create_kpi_card("Completed", str(completed_tasks), f"{completion_rate:.1f}%", "#43A047")
        
        # Display upcoming tasks
        st.subheader("Upcoming Tasks")
        
        # Get legacy task data for visualization until we have enough data
        if total_tasks == 0:
            task_data = get_task_data(department=department, staff=full_name)
            
            # Show task table if we have legacy data
            if not task_data.empty:
                st.dataframe(task_data[['task_id', 'task_name', 'status', 'priority', 'due_date']], use_container_width=True)
            else:
                st.info("No upcoming tasks found.")
        else:
            # Sort tasks by priority and due date
            sorted_tasks = sorted(
                [t for t in my_tasks if t["status"] != "Completed"],
                key=lambda x: (["Critical", "High", "Medium", "Low"].index(x["priority"]), x["due_date"])
            )
            
            if sorted_tasks:
                for task in sorted_tasks[:5]:  # Show top 5 upcoming tasks
                    st.markdown(
                        f"**{task['task_id']}** - {task['task_name']} - **Priority:** {task['priority']} - "
                        f"**Due:** {task['due_date']}"
                    )
            else:
                st.info("No upcoming tasks found.")
    
    # Manage My Tasks Tab
    with dashboard_tabs[1]:
        st.subheader("My Tasks")
        
        # Display the task list interface for current user's tasks
        display_task_list()
    
    # Performance Metrics Tab
    with dashboard_tabs[2]:
        st.subheader("My Performance")
        
        # Get tasks for performance calculation
        if total_tasks > 0:
            # Calculate real metrics from task data
            completed_on_time = len([
                t for t in my_tasks 
                if t["status"] == "Completed" and 
                (t["completed_date"] <= t["due_date"] if t["completed_date"] else False)
            ])
            
            completion_rate = (completed_tasks / total_tasks) * 100
            on_time_rate = (completed_on_time / completed_tasks) * 100 if completed_tasks > 0 else 0
            critical_tasks_completed = len([
                t for t in my_tasks 
                if t["status"] == "Completed" and t["priority"] == "Critical"
            ])
            
            # Create performance metrics display
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Task Completion Rate", f"{completion_rate:.1f}%")
                st.metric("On-Time Completion", f"{on_time_rate:.1f}%")
            
            with col2:
                st.metric("Critical Tasks Completed", critical_tasks_completed)
                st.metric("Tasks In Progress", in_progress_tasks)
        
        # Create a performance chart (still using mock data until we have enough historical data)
        performance_data = {
            'date': pd.date_range(start='2023-01-01', periods=30, freq='D'),
            'tasks_completed': np.random.randint(0, 5, 30).cumsum(),
            'efficiency_score': [min(100, max(60, 75 + np.random.randint(-10, 10))) for _ in range(30)]
        }
        
        performance_df = pd.DataFrame(performance_data)
        
        # Plot performance trend
        fig = px.line(
            performance_df, 
            x='date', 
            y=['tasks_completed', 'efficiency_score'],
            title="My Performance Trends"
        )
        st.plotly_chart(fig, use_container_width=True)
