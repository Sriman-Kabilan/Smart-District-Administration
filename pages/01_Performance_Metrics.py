import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_handler import get_performance_data
from utils.kpi_calculations import calculate_performance_metrics, calculate_department_comparison

# Configure page
st.set_page_config(
    page_title="Performance Metrics - District Admin",
    page_icon="📊",
    layout="wide"
)

# Authentication check
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to access this page")
    st.stop()

# Page title
st.title("📊 Performance Metrics")
st.write("Analyze performance metrics across departments and staff")

# Sidebar for filtering
with st.sidebar:
    st.header("Filter Options")
    
    # Department filter
    if st.session_state.user_role == "administrator":
        departments = ["All Departments", "Public Works", "Health Services", "Education", "Transportation", "Security"]
        selected_department = st.selectbox("Select Department", departments)
    else:
        from auth import get_user_department
        selected_department = get_user_department()
        st.info(f"Viewing data for: {selected_department}")
    
    # Time period filter
    time_periods = ["Last Month", "Last Quarter", "Last Year"]
    selected_time = st.selectbox("Time Period", time_periods)
    
    # Metric type filter
    metric_types = ["Efficiency", "Task Completion", "Resource Utilization", "Citizen Satisfaction"]
    selected_metrics = st.multiselect("Metrics to Display", metric_types, default=["Efficiency", "Task Completion"])

# Main content
if selected_department == "All Departments" and st.session_state.user_role == "administrator":
    # Department comparison
    st.subheader("Department Performance Comparison")
    
    # Get comparison data
    comparison_data = calculate_department_comparison()
    
    # Create comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Performance score comparison
        fig = px.bar(
            comparison_data,
            x='department',
            y='performance_score',
            color='performance_score',
            color_continuous_scale='Blues',
            title="Performance Score by Department"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Satisfaction score comparison
        fig2 = px.bar(
            comparison_data,
            x='department',
            y='satisfaction_score',
            color='satisfaction_score',
            color_continuous_scale='Greens',
            title="Citizen Satisfaction by Department"
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Resource efficiency comparison
    fig3 = px.bar(
        comparison_data,
        x='department',
        y='resource_efficiency',
        color='resource_efficiency',
        color_continuous_scale='Oranges',
        title="Resource Efficiency by Department"
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    # Detailed metrics table
    st.subheader("Detailed Metrics by Department")
    st.dataframe(comparison_data, use_container_width=True)
    
else:
    # Single department view
    department = selected_department if selected_department != "All Departments" else "Public Works"
    
    # Get performance data
    performance_data = get_performance_data(department=department)
    
    # Calculate department metrics
    metrics = calculate_performance_metrics(department)
    
    # Display KPI cards
    st.subheader(f"{department} Performance Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Performance Score", f"{metrics['performance_score']}/100", f"{metrics['performance_trend']}%")
    
    with col2:
        st.metric("Budget Utilization", f"{metrics['budget_utilization']}%", f"{metrics['budget_trend']}%")
    
    with col3:
        st.metric("Staff Count", metrics['staff_count'], "")
    
    with col4:
        st.metric("Open Tasks", metrics['open_tasks'], f"{metrics['task_trend']}%")
    
    # Performance trends
    st.subheader("Performance Trends")
    
    # Create line chart for performance metrics over time
    fig = px.line(
        performance_data,
        x='month',
        y=['efficiency_score', 'task_completion_rate'],
        title=f"{department} Performance Trends",
        labels={'value': 'Score', 'variable': 'Metric'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Staff performance section
    st.subheader("Staff Performance")
    
    # Get staff performance data
    staff_data = get_performance_data(department=department, by_staff=True)
    
    # Staff efficiency bar chart
    fig2 = px.bar(
        staff_data,
        x='staff_name',
        y='efficiency_score',
        color='efficiency_score',
        color_continuous_scale='Blues',
        title="Staff Efficiency Scores"
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Tasks completed by staff
    fig3 = px.bar(
        staff_data,
        x='staff_name',
        y='tasks_completed',
        color='tasks_completed',
        color_continuous_scale='Greens',
        title="Tasks Completed by Staff"
    )
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)
    
    # Additional insights
    st.subheader("Performance Insights")
    
    # Calculate top performer
    top_performer = staff_data.loc[staff_data['efficiency_score'].idxmax()]
    
    # Display insights
    st.info(f"Top Performer: {top_performer['staff_name']} with efficiency score of {top_performer['efficiency_score']}")
    
    # Calculate performance distribution
    low_performers = len(staff_data[staff_data['efficiency_score'] < 70])
    mid_performers = len(staff_data[(staff_data['efficiency_score'] >= 70) & (staff_data['efficiency_score'] < 85)])
    high_performers = len(staff_data[staff_data['efficiency_score'] >= 85])
    
    # Display distribution
    st.write(f"Performance Distribution: {high_performers} high performers, {mid_performers} mid performers, {low_performers} low performers")
