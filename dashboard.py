import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from datetime import datetime, timedelta
from utils.data_handler import get_department_data, get_performance_data, get_resource_data, get_task_data
from utils.visualization import create_kpi_card, create_performance_chart, create_resource_chart
from utils.kpi_calculations import calculate_performance_metrics

# Admin Dashboard
def display_admin_dashboard():
    st.title("District Administration Dashboard")
    st.write(f"Welcome, {st.session_state.username} (Administrator)")
    
    # Overview metrics
    st.subheader("District Overview")
    
    # KPI metrics row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        create_kpi_card("Total Departments", "5", "10% ↑", "#1E88E5")
    
    with kpi2:
        create_kpi_card("Open Tasks", "42", "5% ↓", "#43A047")
    
    with kpi3:
        create_kpi_card("Resource Utilization", "78%", "3% ↑", "#FB8C00") 
    
    with kpi4:
        create_kpi_card("Citizen Satisfaction", "86%", "2% ↑", "#8E24AA")
    
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
    
    # Recent activity section
    st.subheader("Recent System Activity")
    
    if "activity_log" in st.session_state:
        activity_df = pd.DataFrame(st.session_state.activity_log[-10:])
        if not activity_df.empty:
            st.dataframe(activity_df, use_container_width=True)
        else:
            st.info("No activity recorded yet")
    else:
        st.info("No activity recorded yet")

# Department Head Dashboard
def display_department_head_dashboard():
    from auth import get_user_department
    
    department = get_user_department()
    
    st.title(f"{department} Department Dashboard")
    st.write(f"Welcome, {st.session_state.username} (Department Head)")
    
    # Overview metrics for the department
    st.subheader("Department Overview")
    
    # Calculate department metrics
    performance_metrics = calculate_performance_metrics(department)
    
    # KPI metrics row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        create_kpi_card("Staff Members", str(performance_metrics['staff_count']), "", "#1E88E5")
    
    with kpi2:
        create_kpi_card("Open Tasks", str(performance_metrics['open_tasks']), f"{performance_metrics['task_trend']}% {'↑' if performance_metrics['task_trend'] > 0 else '↓'}", "#43A047")
    
    with kpi3:
        create_kpi_card("Budget Utilized", f"{performance_metrics['budget_utilization']}%", f"{performance_metrics['budget_trend']}% {'↑' if performance_metrics['budget_trend'] > 0 else '↓'}", "#FB8C00") 
    
    with kpi4:
        create_kpi_card("Performance Score", f"{performance_metrics['performance_score']}/100", f"{performance_metrics['performance_trend']}% {'↑' if performance_metrics['performance_trend'] > 0 else '↓'}", "#8E24AA")
    
    # Department specific performance
    st.subheader("Department Performance")
    
    # Get department data
    department_data = get_department_data(department)
    
    # Create performance charts
    col1, col2 = st.columns(2)
    
    with col1:
        chart = create_performance_chart(department_data, "weekly")
        st.altair_chart(chart, use_container_width=True)
    
    with col2:
        resource_chart = create_resource_chart(department_data)
        st.altair_chart(resource_chart, use_container_width=True)
    
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
    
    # Task status section
    st.subheader("Task Status")
    
    # Get task data
    task_data = get_task_data(department=department)
    
    # Show task table
    st.dataframe(task_data[['task_id', 'task_name', 'assigned_to', 'status', 'due_date']], use_container_width=True)

# Staff Dashboard
def display_staff_dashboard():
    from auth import get_user_department, get_user_fullname
    
    department = get_user_department()
    full_name = get_user_fullname()
    
    st.title("Staff Dashboard")
    st.write(f"Welcome, {full_name} ({department})")
    
    # My Tasks section
    st.subheader("My Tasks")
    
    # Get tasks assigned to the current user
    task_data = get_task_data(department=department, staff=full_name)
    
    # Task counts
    total_tasks = len(task_data)
    completed_tasks = len(task_data[task_data['status'] == 'Completed'])
    in_progress_tasks = len(task_data[task_data['status'] == 'In Progress'])
    pending_tasks = len(task_data[task_data['status'] == 'Pending'])
    
    # Task KPI metrics row
    kpi1, kpi2, kpi3 = st.columns(3)
    
    with kpi1:
        create_kpi_card("Pending Tasks", str(pending_tasks), "", "#FB8C00")
    
    with kpi2:
        create_kpi_card("In Progress", str(in_progress_tasks), "", "#1E88E5")
    
    with kpi3:
        create_kpi_card("Completed", str(completed_tasks), "", "#43A047")
    
    # Task table with mock update functionality
    st.subheader("Task List")
    
    # Display tasks in a more interactive way
    for index, task in task_data.iterrows():
        with st.expander(f"{task['task_name']} - {task['status']}"):
            st.write(f"**Task ID:** {task['task_id']}")
            st.write(f"**Description:** {task['description']}")
            st.write(f"**Due Date:** {task['due_date']}")
            st.write(f"**Priority:** {task['priority']}")
            
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
    
    # Performance metrics
    st.subheader("My Performance")
    
    # Create a simple performance chart
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
