import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_handler import get_task_data

# Configure page
st.set_page_config(
    page_title="Task Tracking - District Admin",
    page_icon="✅",
    layout="wide"
)

# Authentication check
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to access this page")
    st.stop()

# Page title
st.title("✅ Task Tracking")
st.write("Monitor and manage tasks across departments")

# Sidebar for filtering
with st.sidebar:
    st.header("Filter Options")
    
    # Department filter
    if st.session_state.user_role == "administrator":
        departments = ["All Departments", "Public Works", "Health Services", "Education", "Transportation", "Security"]
        selected_department = st.selectbox("Select Department", departments)
    else:
        from auth import get_user_department, get_user_fullname
        selected_department = get_user_department()
        st.info(f"Viewing data for: {selected_department}")
    
    # Status filter
    statuses = ["All Statuses", "Pending", "In Progress", "Completed"]
    selected_status = st.selectbox("Task Status", statuses)
    
    # Priority filter
    priorities = ["All Priorities", "Low", "Medium", "High", "Critical"]
    selected_priority = st.selectbox("Task Priority", priorities)
    
    # Date range filter
    st.write("Due Date Range")
    start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    end_date = st.date_input("End Date", datetime.now() + timedelta(days=30))

# Function to apply filters to task data
def apply_filters(task_data):
    filtered_data = task_data.copy()
    
    # Filter by status
    if selected_status != "All Statuses":
        filtered_data = filtered_data[filtered_data['status'] == selected_status]
    
    # Filter by priority
    if selected_priority != "All Priorities":
        filtered_data = filtered_data[filtered_data['priority'] == selected_priority]
    
    # Filter by date range
    filtered_data['due_date'] = pd.to_datetime(filtered_data['due_date'])
    filtered_data = filtered_data[
        (filtered_data['due_date'] >= pd.Timestamp(start_date)) & 
        (filtered_data['due_date'] <= pd.Timestamp(end_date))
    ]
    
    return filtered_data

# Main content
if selected_department == "All Departments" and st.session_state.user_role == "administrator":
    # District-wide task overview
    st.subheader("District-wide Task Overview")
    
    # Get task data for all departments
    all_departments = ["Public Works", "Health Services", "Education", "Transportation", "Security"]
    all_tasks = pd.DataFrame()
    
    for dept in all_departments:
        dept_tasks = get_task_data(department=dept)
        all_tasks = pd.concat([all_tasks, dept_tasks])
    
    # Apply filters
    filtered_tasks = apply_filters(all_tasks)
    
    # Task status summary
    status_counts = filtered_tasks['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    
    # Create status pie chart
    fig = px.pie(
        status_counts,
        values='count',
        names='status',
        title="Task Status Distribution",
        color='status',
        color_discrete_map={
            'Pending': '#FFC107',
            'In Progress': '#2196F3',
            'Completed': '#4CAF50'
        }
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Tasks by department
    dept_counts = filtered_tasks.groupby(['department', 'status']).size().reset_index(name='count')
    
    # Create department bar chart
    fig2 = px.bar(
        dept_counts,
        x='department',
        y='count',
        color='status',
        title="Tasks by Department and Status",
        color_discrete_map={
            'Pending': '#FFC107',
            'In Progress': '#2196F3',
            'Completed': '#4CAF50'
        }
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Priority distribution
    priority_counts = filtered_tasks.groupby(['priority', 'status']).size().reset_index(name='count')
    
    # Create priority bar chart
    fig3 = px.bar(
        priority_counts,
        x='priority',
        y='count',
        color='status',
        title="Tasks by Priority and Status",
        color_discrete_map={
            'Pending': '#FFC107',
            'In Progress': '#2196F3',
            'Completed': '#4CAF50'
        },
        category_orders={"priority": ["Low", "Medium", "High", "Critical"]}
    )
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)
    
    # Task details table
    st.subheader("Task Details")
    
    # Create tabs for different task views
    task_tabs = st.tabs(["All Tasks", "Pending Tasks", "Overdue Tasks"])
    
    with task_tabs[0]:
        st.dataframe(
            filtered_tasks[['task_id', 'task_name', 'department', 'assigned_to', 'status', 'priority', 'due_date']], 
            use_container_width=True
        )
    
    with task_tabs[1]:
        pending_tasks = filtered_tasks[filtered_tasks['status'] == 'Pending']
        st.dataframe(
            pending_tasks[['task_id', 'task_name', 'department', 'assigned_to', 'priority', 'due_date']], 
            use_container_width=True
        )
    
    with task_tabs[2]:
        # Calculate overdue tasks
        today = pd.Timestamp(datetime.now().date())
        overdue_tasks = filtered_tasks[
            (filtered_tasks['due_date'] < today) & 
            (filtered_tasks['status'] != 'Completed')
        ]
        
        if not overdue_tasks.empty:
            st.dataframe(
                overdue_tasks[['task_id', 'task_name', 'department', 'assigned_to', 'status', 'priority', 'due_date']], 
                use_container_width=True
            )
        else:
            st.info("No overdue tasks found.")
    
else:
    # Single department view
    department = selected_department if selected_department != "All Departments" else "Public Works"
    
    # Get staff name for individual view
    if st.session_state.user_role == "staff":
        from auth import get_user_fullname
        staff_name = get_user_fullname()
        st.subheader(f"Tasks for {staff_name}")
        
        # Get tasks for this staff member
        task_data = get_task_data(department=department, staff=staff_name)
    else:
        st.subheader(f"{department} Department Tasks")
        
        # Get all tasks for the department
        task_data = get_task_data(department=department)
    
    # Apply filters
    filtered_tasks = apply_filters(task_data)
    
    # Task summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pending_count = len(filtered_tasks[filtered_tasks['status'] == 'Pending'])
        st.metric("Pending Tasks", pending_count)
    
    with col2:
        in_progress_count = len(filtered_tasks[filtered_tasks['status'] == 'In Progress'])
        st.metric("In Progress", in_progress_count)
    
    with col3:
        completed_count = len(filtered_tasks[filtered_tasks['status'] == 'Completed'])
        st.metric("Completed Tasks", completed_count)
    
    # Task status distribution
    status_counts = filtered_tasks['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    
    # Create status pie chart
    fig = px.pie(
        status_counts,
        values='count',
        names='status',
        title="Task Status Distribution",
        color='status',
        color_discrete_map={
            'Pending': '#FFC107',
            'In Progress': '#2196F3',
            'Completed': '#4CAF50'
        }
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)
    
    # Create task management section
    st.subheader("Task Management")
    
    # Create tabs for different task views
    task_tabs = st.tabs(["All Tasks", "Pending Tasks", "In Progress", "Completed"])
    
    with task_tabs[0]:
        # All tasks
        if not filtered_tasks.empty:
            for index, task in filtered_tasks.iterrows():
                with st.expander(f"{task['task_name']} - {task['status']}"):
                    st.write(f"**Task ID:** {task['task_id']}")
                    st.write(f"**Description:** {task['description']}")
                    st.write(f"**Assigned To:** {task['assigned_to']}")
                    st.write(f"**Priority:** {task['priority']}")
                    st.write(f"**Start Date:** {task['start_date']}")
                    st.write(f"**Due Date:** {task['due_date']}")
                    
                    # Add status update option
                    new_status = st.selectbox(
                        "Update Status:",
                        options=["Pending", "In Progress", "Completed"],
                        index=["Pending", "In Progress", "Completed"].index(task['status']),
                        key=f"status_{task['task_id']}"
                    )
                    
                    if st.button("Update", key=f"update_{task['task_id']}"):
                        st.success(f"Status updated to {new_status}")
                        # In a real application, this would update the database
        else:
            st.info("No tasks match the selected filters.")
    
    with task_tabs[1]:
        # Pending tasks
        pending_tasks = filtered_tasks[filtered_tasks['status'] == 'Pending']
        if not pending_tasks.empty:
            for index, task in pending_tasks.iterrows():
                with st.expander(f"{task['task_name']} - Due: {task['due_date']}"):
                    st.write(f"**Task ID:** {task['task_id']}")
                    st.write(f"**Description:** {task['description']}")
                    st.write(f"**Assigned To:** {task['assigned_to']}")
                    st.write(f"**Priority:** {task['priority']}")
                    
                    if st.button("Start Task", key=f"start_{task['task_id']}"):
                        st.success("Task status updated to In Progress")
                        # In a real application, this would update the database
        else:
            st.info("No pending tasks match the selected filters.")
    
    with task_tabs[2]:
        # In progress tasks
        in_progress_tasks = filtered_tasks[filtered_tasks['status'] == 'In Progress']
        if not in_progress_tasks.empty:
            for index, task in in_progress_tasks.iterrows():
                with st.expander(f"{task['task_name']} - Due: {task['due_date']}"):
                    st.write(f"**Task ID:** {task['task_id']}")
                    st.write(f"**Description:** {task['description']}")
                    st.write(f"**Assigned To:** {task['assigned_to']}")
                    st.write(f"**Priority:** {task['priority']}")
                    
                    if st.button("Complete Task", key=f"complete_{task['task_id']}"):
                        st.success("Task status updated to Completed")
                        # In a real application, this would update the database
        else:
            st.info("No in-progress tasks match the selected filters.")
    
    with task_tabs[3]:
        # Completed tasks
        completed_tasks = filtered_tasks[filtered_tasks['status'] == 'Completed']
        if not completed_tasks.empty:
            for index, task in completed_tasks.iterrows():
                with st.expander(f"{task['task_name']} - Completed"):
                    st.write(f"**Task ID:** {task['task_id']}")
                    st.write(f"**Description:** {task['description']}")
                    st.write(f"**Assigned To:** {task['assigned_to']}")
                    st.write(f"**Priority:** {task['priority']}")
                    st.write(f"**Due Date:** {task['due_date']}")
        else:
            st.info("No completed tasks match the selected filters.")
    
    # Add new task section (visible only to administrators and department heads)
    if st.session_state.user_role in ["administrator", "department_head"]:
        st.subheader("Add New Task")
        
        # Create form for new task
        with st.form("new_task_form"):
            task_name = st.text_input("Task Name")
            task_description = st.text_area("Task Description")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Get staff for the department
                if department == "Public Works":
                    staff_list = ["John Smith", "Maria Garcia", "Robert Johnson", "Lisa Wong"]
                elif department == "Health Services":
                    staff_list = ["David Lee", "Sarah Johnson", "Michael Brown", "Jessica Williams"]
                elif department == "Education":
                    staff_list = ["James Wilson", "Emily Davis", "Thomas Moore", "Jennifer Martin"]
                elif department == "Transportation":
                    staff_list = ["Daniel Rodriguez", "Amanda Clark", "William Taylor", "Elizabeth Lewis"]
                elif department == "Security":
                    staff_list = ["Richard Harris", "Patricia Martinez", "Charles Thompson", "Susan Anderson"]
                else:
                    staff_list = ["Staff Member 1", "Staff Member 2", "Staff Member 3", "Staff Member 4"]
                
                assigned_to = st.selectbox("Assign To", staff_list)
                priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            
            with col2:
                start_date = st.date_input("Start Date", datetime.now())
                due_date = st.date_input("Due Date", datetime.now() + timedelta(days=7))
            
            submitted = st.form_submit_button("Add Task")
            
            if submitted:
                st.success(f"Task '{task_name}' would be added and assigned to {assigned_to}")
                st.info("This is a demo. In a real application, this would add a task to the database.")
