import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_handler import get_resource_data
from utils.kpi_calculations import calculate_resource_efficiency

# Configure page
st.set_page_config(
    page_title="Resource Management - District Admin",
    page_icon="📦",
    layout="wide"
)

# Authentication check
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to access this page")
    st.stop()

# Page title
st.title("📦 Resource Management")
st.write("Track and manage resources across departments")

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
    
    # Resource type filter
    resource_types = ["Budget", "Personnel", "Equipment", "All Resources"]
    selected_resource = st.selectbox("Resource Type", resource_types)
    
    # Time period filter
    time_periods = ["Current Quarter", "Year to Date", "Annual Budget"]
    selected_period = st.selectbox("Budget Period", time_periods)

# Main content
if selected_department == "All Departments" and st.session_state.user_role == "administrator":
    # District-wide resource overview
    st.subheader("District-wide Resource Allocation")
    
    # Get resource data for all departments
    resource_data = get_resource_data(all_departments=True)
    
    # Create budget allocation chart
    fig = px.pie(
        resource_data,
        values='budget_allocation',
        names='department',
        title="Budget Allocation by Department",
        hole=0.4
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Create budget utilization chart
    fig2 = px.bar(
        resource_data,
        x='department',
        y=['budget_allocation', 'budget_spent'],
        title="Budget Allocation vs Spent by Department",
        barmode='group',
        labels={'value': 'Amount', 'variable': 'Category'}
    )
    fig2.update_layout(height=500)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Calculate resource efficiency for all departments
    efficiency_data = []
    for dept in resource_data['department'].unique():
        efficiency = calculate_resource_efficiency(department=dept)
        efficiency_data.append({
            'department': dept,
            'budget_efficiency': efficiency['budget_efficiency'],
            'staff_efficiency': efficiency['staff_efficiency'],
            'equipment_efficiency': efficiency['equipment_efficiency'],
            'overall_efficiency': efficiency['overall_efficiency']
        })
    
    efficiency_df = pd.DataFrame(efficiency_data)
    
    # Create efficiency comparison chart
    fig3 = px.bar(
        efficiency_df,
        x='department',
        y=['budget_efficiency', 'staff_efficiency', 'equipment_efficiency'],
        title="Resource Efficiency by Department",
        barmode='group',
        labels={'value': 'Efficiency Score', 'variable': 'Resource Type'}
    )
    fig3.update_layout(height=500)
    st.plotly_chart(fig3, use_container_width=True)
    
    # Display resource data table
    st.subheader("Resource Allocation Details")
    
    # Combine data
    merged_data = pd.merge(resource_data, efficiency_df, on='department')
    st.dataframe(merged_data, use_container_width=True)
    
    # Resource utilization insights
    st.subheader("Resource Utilization Insights")
    
    # Calculate insights
    total_budget = resource_data['budget_allocation'].sum()
    total_spent = resource_data['budget_spent'].sum()
    utilization_rate = (total_spent / total_budget) * 100
    
    # Display insights
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Budget", f"${total_budget:,.2f}")
    with col2:
        st.metric("Total Spent", f"${total_spent:,.2f}")
    with col3:
        st.metric("Utilization Rate", f"{utilization_rate:.1f}%")
    
    # Department with highest and lowest utilization
    resource_data['utilization_rate'] = (resource_data['budget_spent'] / resource_data['budget_allocation']) * 100
    highest_util = resource_data.loc[resource_data['utilization_rate'].idxmax()]
    lowest_util = resource_data.loc[resource_data['utilization_rate'].idxmin()]
    
    st.info(f"Highest Utilization: {highest_util['department']} ({highest_util['utilization_rate']:.1f}%)")
    st.info(f"Lowest Utilization: {lowest_util['department']} ({lowest_util['utilization_rate']:.1f}%)")
    
else:
    # Single department view
    department = selected_department if selected_department != "All Departments" else "Public Works"
    
    # Get detailed resource data for the department
    resource_data = get_resource_data(department=department)
    
    # Get resource efficiency metrics
    efficiency = calculate_resource_efficiency(department=department)
    
    # Display KPI cards
    st.subheader(f"{department} Resource Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Efficiency", f"{efficiency['overall_efficiency']}%", "")
    
    with col2:
        st.metric("Budget Efficiency", f"{efficiency['budget_efficiency']}%", f"{efficiency['budget_trend']}%")
    
    with col3:
        st.metric("Staff Efficiency", f"{efficiency['staff_efficiency']}%", f"{efficiency['staff_trend']}%")
    
    with col4:
        st.metric("Equipment Efficiency", f"{efficiency['equipment_efficiency']}%", f"{efficiency['equipment_trend']}%")
    
    # Resource allocation by category
    st.subheader("Resource Allocation by Category")
    
    # Create resource allocation chart
    fig = px.pie(
        resource_data,
        values='allocation',
        names='category',
        title=f"{department} Resource Allocation by Category",
        color_discrete_sequence=px.colors.sequential.Blues
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Budget spent vs allocated
    st.subheader("Budget Allocated vs Spent")
    
    # Create comparison chart
    fig2 = px.bar(
        resource_data,
        x='category',
        y=['allocation', 'spent', 'remaining'],
        title=f"{department} Budget Allocation and Spending",
        barmode='group',
        labels={'value': 'Amount', 'variable': 'Category'}
    )
    fig2.update_layout(height=500)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Resource utilization table
    st.subheader("Resource Utilization Details")
    
    # Calculate utilization percentage
    resource_data['utilization_pct'] = (resource_data['spent'] / resource_data['allocation']) * 100
    
    # Display table
    st.dataframe(resource_data, use_container_width=True)
    
    # Resource management actions
    st.subheader("Resource Management Actions")
    
    # Create two columns for actions
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        st.write("Budget Reallocation")
        
        # Select category to adjust
        categories = resource_data['category'].tolist()
        adjust_category = st.selectbox("Select Category", categories)
        
        # Get current allocation
        current_allocation = resource_data.loc[resource_data['category'] == adjust_category, 'allocation'].iloc[0]
        
        # Adjustment amount
        new_allocation = st.number_input(
            "New Allocation Amount",
            min_value=0.0,
            max_value=float(current_allocation * 2),
            value=float(current_allocation),
            step=1000.0
        )
        
        if st.button("Update Allocation"):
            st.success(f"Budget for {adjust_category} would be updated from ${current_allocation:,.2f} to ${new_allocation:,.2f}")
            st.info("This is a demo. In a real application, this would update the database.")
    
    with action_col2:
        st.write("Resource Efficiency Improvement")
        
        # Select area to improve
        improvement_areas = ["Budget Utilization", "Staff Allocation", "Equipment Maintenance"]
        area_to_improve = st.selectbox("Select Area for Improvement", improvement_areas)
        
        # Suggested actions
        if area_to_improve == "Budget Utilization":
            st.info("Suggested Actions:")
            st.write("1. Review spending patterns in low-utilization categories")
            st.write("2. Reallocate funds from underutilized categories")
            st.write("3. Implement monthly budget reviews")
        elif area_to_improve == "Staff Allocation":
            st.info("Suggested Actions:")
            st.write("1. Analyze staff workload distribution")
            st.write("2. Identify opportunities for cross-training")
            st.write("3. Adjust staff allocation based on project priorities")
        else:
            st.info("Suggested Actions:")
            st.write("1. Schedule regular equipment maintenance")
            st.write("2. Track equipment utilization rates")
            st.write("3. Develop equipment replacement schedule")
        
        if st.button("Generate Improvement Plan"):
            st.success(f"Improvement plan for {area_to_improve} would be generated")
            st.info("This is a demo. In a real application, this would generate a detailed plan.")
