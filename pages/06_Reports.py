import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_handler import get_performance_data, get_resource_data, get_task_data, get_department_data
from utils.kpi_calculations import calculate_performance_metrics, calculate_department_comparison, calculate_satisfaction_metrics

# Configure page
st.set_page_config(
    page_title="Reports - District Admin",
    page_icon="📊",
    layout="wide"
)

# Authentication check
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to access this page")
    st.stop()

# Page title
st.title("📊 Reports")
st.write("Generate and export reports for various district metrics")

# Sidebar for report options
with st.sidebar:
    st.header("Report Options")
    
    # Report type selection
    report_types = [
        "Department Performance", 
        "Resource Utilization", 
        "Task Completion", 
        "Citizen Satisfaction",
        "Budget Analysis",
        "Cross-Department Comparison"
    ]
    selected_report = st.selectbox("Report Type", report_types)
    
    # Department filter (if administrator)
    if st.session_state.user_role == "administrator":
        departments = ["All Departments", "Public Works", "Health Services", "Education", "Transportation", "Security"]
        selected_department = st.selectbox("Department", departments)
    else:
        from auth import get_user_department
        selected_department = get_user_department()
        st.info(f"Viewing data for: {selected_department}")
    
    # Time period selection
    time_periods = ["Last Month", "Last Quarter", "Last 6 Months", "Year to Date", "Annual"]
    selected_period = st.selectbox("Time Period", time_periods)
    
    # Report format
    report_formats = ["Interactive Dashboard", "Summary View"]
    selected_format = st.selectbox("Report Format", report_formats)
    
    # Generate report button
    generate_button = st.button("Generate Report")

# Helper function to map time period to days
def map_time_period_to_days(period):
    if period == "Last Month":
        return 30
    elif period == "Last Quarter":
        return 90
    elif period == "Last 6 Months":
        return 180
    elif period == "Year to Date":
        return 365
    elif period == "Annual":
        return 365
    else:
        return 30  # Default to a month

# Helper function to get date range string for the selected period
def get_date_range_string(period):
    today = datetime.now()
    
    if period == "Last Month":
        start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
    elif period == "Last Quarter":
        start_date = (today - timedelta(days=90)).strftime('%Y-%m-%d')
    elif period == "Last 6 Months":
        start_date = (today - timedelta(days=180)).strftime('%Y-%m-%d')
    elif period == "Year to Date":
        start_date = datetime(today.year, 1, 1).strftime('%Y-%m-%d')
    elif period == "Annual":
        start_date = (today - timedelta(days=365)).strftime('%Y-%m-%d')
    else:
        start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
    
    end_date = today.strftime('%Y-%m-%d')
    return f"{start_date} to {end_date}"

# Helper function to format numbers for display
def format_number(number, is_currency=False, is_percentage=False):
    if is_currency:
        return f"${number:,.2f}"
    elif is_percentage:
        return f"{number:.1f}%"
    else:
        return f"{number:,}"

# Main content area
if generate_button or True:  # Always show some content
    # Report header
    st.header(f"{selected_report} Report")
    st.write(f"Period: {get_date_range_string(selected_period)}")
    
    if selected_department != "All Departments":
        st.write(f"Department: {selected_department}")
    
    # Different report types
    if selected_report == "Department Performance":
        # Department Performance Report
        if selected_department == "All Departments" and st.session_state.user_role == "administrator":
            # Show comparison of all departments
            comparison_data = calculate_department_comparison()
            
            if selected_format == "Interactive Dashboard":
                # Interactive dashboard view
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
                    # Resource efficiency comparison
                    fig2 = px.bar(
                        comparison_data,
                        x='department',
                        y='resource_efficiency',
                        color='resource_efficiency',
                        color_continuous_scale='Greens',
                        title="Resource Efficiency by Department"
                    )
                    fig2.update_layout(height=400)
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Satisfaction scores
                fig3 = px.bar(
                    comparison_data,
                    x='department',
                    y='satisfaction_score',
                    color='department',
                    title="Citizen Satisfaction Score by Department"
                )
                st.plotly_chart(fig3, use_container_width=True)
                
                # Data table
                st.subheader("Detailed Performance Metrics")
                st.dataframe(comparison_data, use_container_width=True)
                
                # Download button
                if st.download_button(
                    label="Download Report Data (CSV)",
                    data=comparison_data.to_csv(index=False).encode('utf-8'),
                    file_name=f"department_performance_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Report data downloaded successfully!")
            
            else:
                # Summary view
                st.subheader("Performance Summary")
                
                # Calculate overall metrics
                avg_performance = comparison_data['performance_score'].mean()
                top_department = comparison_data.loc[comparison_data['performance_score'].idxmax()]
                bottom_department = comparison_data.loc[comparison_data['performance_score'].idxmin()]
                
                # Display summary stats
                st.write(f"**Average Performance Score:** {avg_performance:.1f}/100")
                st.write(f"**Top Performing Department:** {top_department['department']} ({top_department['performance_score']:.1f}/100)")
                st.write(f"**Lowest Performing Department:** {bottom_department['department']} ({bottom_department['performance_score']:.1f}/100)")
                
                # Display the table
                st.subheader("Department Performance Overview")
                st.dataframe(
                    comparison_data[['department', 'performance_score', 'satisfaction_score', 'resource_efficiency']],
                    use_container_width=True
                )
                
                # Executive summary
                st.subheader("Executive Summary")
                st.write(f"""
                This report provides an overview of department performance across the district for the period {get_date_range_string(selected_period)}.
                
                Key findings:
                - Average performance score across all departments is {avg_performance:.1f}/100
                - {top_department['department']} is the top performing department with a score of {top_department['performance_score']:.1f}/100
                - {bottom_department['department']} has the lowest performance with a score of {bottom_department['performance_score']:.1f}/100
                - Overall citizen satisfaction across departments is {comparison_data['satisfaction_score'].mean():.1f}/100
                
                Recommendations:
                - Review resource allocation for {bottom_department['department']} to improve performance
                - Consider implementing best practices from {top_department['department']} across other departments
                - Continue monitoring performance metrics on a regular basis
                """)
                
                # Download button
                if st.download_button(
                    label="Download Summary Report (CSV)",
                    data=comparison_data.to_csv(index=False).encode('utf-8'),
                    file_name=f"department_performance_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Summary report downloaded successfully!")
        
        else:
            # Single department performance report
            department = selected_department if selected_department != "All Departments" else "Public Works"
            
            # Get performance data for this department
            performance_data = get_performance_data(department=department)
            metrics = calculate_performance_metrics(department)
            
            if selected_format == "Interactive Dashboard":
                # Interactive dashboard view
                st.subheader(f"{department} Performance Metrics")
                
                # KPI metrics row
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Performance Score", f"{metrics['performance_score']}/100", f"{metrics['performance_trend']}%")
                
                with col2:
                    st.metric("Budget Utilization", f"{metrics['budget_utilization']}%", f"{metrics['budget_trend']}%")
                
                with col3:
                    st.metric("Task Completion", f"{100 - metrics['open_tasks']}%", f"{metrics['task_trend']}%")
                
                with col4:
                    st.metric("Staff Count", metrics['staff_count'], "")
                
                # Performance trend chart
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
                
                # Staff performance data
                staff_data = get_performance_data(department=department, by_staff=True)
                
                st.subheader("Staff Performance")
                fig2 = px.bar(
                    staff_data,
                    x='staff_name',
                    y='efficiency_score',
                    color='efficiency_score',
                    color_continuous_scale='Blues',
                    title=f"{department} Staff Efficiency Scores"
                )
                st.plotly_chart(fig2, use_container_width=True)
                
                # Download button
                st.subheader("Download Report")
                
                # Combine data for download
                download_data = {
                    'department': department,
                    'period': selected_period,
                    'performance_score': metrics['performance_score'],
                    'budget_utilization': metrics['budget_utilization'],
                    'performance_trend': metrics['performance_trend'],
                    'staff_count': metrics['staff_count'],
                    'open_tasks': metrics['open_tasks'],
                }
                
                download_df = pd.DataFrame([download_data])
                
                if st.download_button(
                    label="Download Performance Report (CSV)",
                    data=download_df.to_csv(index=False).encode('utf-8'),
                    file_name=f"{department}_performance_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Report data downloaded successfully!")
            
            else:
                # Summary view
                st.subheader(f"{department} Performance Summary")
                
                # Display key metrics
                st.write(f"**Performance Score:** {metrics['performance_score']}/100 ({metrics['performance_trend']}% change)")
                st.write(f"**Budget Utilization:** {metrics['budget_utilization']}% ({metrics['budget_trend']}% change)")
                st.write(f"**Staff Count:** {metrics['staff_count']}")
                st.write(f"**Open Tasks:** {metrics['open_tasks']} ({metrics['task_trend']}% change)")
                
                # Staff performance summary
                staff_data = get_performance_data(department=department, by_staff=True)
                
                # Identify top performer
                top_performer = staff_data.loc[staff_data['efficiency_score'].idxmax()]
                
                st.write(f"**Top Performer:** {top_performer['staff_name']} (Efficiency: {top_performer['efficiency_score']:.1f}/100)")
                
                # Calculate performance distribution
                low_performers = len(staff_data[staff_data['efficiency_score'] < 70])
                mid_performers = len(staff_data[(staff_data['efficiency_score'] >= 70) & (staff_data['efficiency_score'] < 85)])
                high_performers = len(staff_data[staff_data['efficiency_score'] >= 85])
                
                st.write(f"**Performance Distribution:** {high_performers} high performers, {mid_performers} mid performers, {low_performers} low performers")
                
                # Summary recommendations
                st.subheader("Recommendations")
                
                if metrics['performance_trend'] < 0:
                    st.write("- Review recent department changes that may have impacted performance")
                
                if metrics['budget_utilization'] < 70:
                    st.write("- Evaluate budget allocation to improve utilization")
                
                if low_performers > 0:
                    st.write(f"- Consider additional training for {low_performers} low-performing staff members")
                
                if metrics['open_tasks'] > 20:
                    st.write("- Implement task prioritization to address high number of open tasks")
                
                # Download button
                summary_data = pd.DataFrame({
                    'Metric': ['Performance Score', 'Budget Utilization', 'Staff Count', 'Open Tasks'],
                    'Value': [
                        f"{metrics['performance_score']}/100",
                        f"{metrics['budget_utilization']}%",
                        f"{metrics['staff_count']}",
                        f"{metrics['open_tasks']}"
                    ],
                    'Change': [
                        f"{metrics['performance_trend']}%",
                        f"{metrics['budget_trend']}%",
                        "",
                        f"{metrics['task_trend']}%"
                    ]
                })
                
                if st.download_button(
                    label="Download Summary Report (CSV)",
                    data=summary_data.to_csv(index=False).encode('utf-8'),
                    file_name=f"{department}_performance_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Summary report downloaded successfully!")
    
    elif selected_report == "Resource Utilization":
        # Resource Utilization Report
        if selected_department == "All Departments" and st.session_state.user_role == "administrator":
            # Get resource data for all departments
            resource_data = get_resource_data(all_departments=True)
            
            if selected_format == "Interactive Dashboard":
                # Interactive dashboard view
                st.subheader("District-wide Resource Utilization")
                
                # Budget allocation chart
                fig = px.pie(
                    resource_data,
                    values='budget_allocation',
                    names='department',
                    title="Budget Allocation by Department",
                    hole=0.4
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                # Budget allocation vs spent
                fig2 = px.bar(
                    resource_data,
                    x='department',
                    y=['budget_allocation', 'budget_spent'],
                    title="Budget Allocation vs Spent by Department",
                    barmode='group',
                    labels={'value': 'Amount', 'variable': 'Category'}
                )
                st.plotly_chart(fig2, use_container_width=True)
                
                # Calculate utilization percentages
                resource_data['utilization_percentage'] = (resource_data['budget_spent'] / resource_data['budget_allocation'] * 100).round(1)
                
                # Utilization percentage chart
                fig3 = px.bar(
                    resource_data,
                    x='department',
                    y='utilization_percentage',
                    color='utilization_percentage',
                    color_continuous_scale='Greens',
                    title="Budget Utilization Percentage by Department",
                    labels={'utilization_percentage': 'Utilization %'}
                )
                st.plotly_chart(fig3, use_container_width=True)
                
                # Resource data table
                st.subheader("Resource Allocation Details")
                st.dataframe(resource_data, use_container_width=True)
                
                # Download button
                if st.download_button(
                    label="Download Resource Report (CSV)",
                    data=resource_data.to_csv(index=False).encode('utf-8'),
                    file_name=f"resource_utilization_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Report data downloaded successfully!")
            
            else:
                # Summary view
                st.subheader("Resource Utilization Summary")
                
                # Calculate key metrics
                total_budget = resource_data['budget_allocation'].sum()
                total_spent = resource_data['budget_spent'].sum()
                overall_utilization = (total_spent / total_budget * 100).round(1)
                
                # Calculate utilization percentages
                resource_data['utilization_percentage'] = (resource_data['budget_spent'] / resource_data['budget_allocation'] * 100).round(1)
                
                highest_util = resource_data.loc[resource_data['utilization_percentage'].idxmax()]
                lowest_util = resource_data.loc[resource_data['utilization_percentage'].idxmin()]
                
                # Display summary stats
                st.write(f"**Total Budget Allocation:** {format_number(total_budget, is_currency=True)}")
                st.write(f"**Total Budget Spent:** {format_number(total_spent, is_currency=True)}")
                st.write(f"**Overall Utilization Rate:** {overall_utilization}%")
                st.write(f"**Department with Highest Utilization:** {highest_util['department']} ({highest_util['utilization_percentage']}%)")
                st.write(f"**Department with Lowest Utilization:** {lowest_util['department']} ({lowest_util['utilization_percentage']}%)")
                
                # Resource utilization table
                st.subheader("Department Utilization Overview")
                
                # Create a summary table
                summary_table = resource_data[['department', 'budget_allocation', 'budget_spent', 'utilization_percentage']]
                summary_table = summary_table.sort_values('utilization_percentage', ascending=False)
                
                # Format currency columns
                summary_table['budget_allocation'] = summary_table['budget_allocation'].apply(lambda x: format_number(x, is_currency=True))
                summary_table['budget_spent'] = summary_table['budget_spent'].apply(lambda x: format_number(x, is_currency=True))
                summary_table['utilization_percentage'] = summary_table['utilization_percentage'].apply(lambda x: f"{x}%")
                
                st.dataframe(summary_table, use_container_width=True)
                
                # Recommendations
                st.subheader("Recommendations")
                
                if overall_utilization < 70:
                    st.write("- Review overall budget allocation process to improve utilization rates")
                
                if lowest_util['utilization_percentage'] < 60:
                    st.write(f"- Evaluate {lowest_util['department']} budget to identify underutilized resources")
                
                if highest_util['utilization_percentage'] > 90:
                    st.write(f"- Consider increasing budget allocation for {highest_util['department']}")
                
                # Add departments with significant deviation from average
                for _, row in resource_data.iterrows():
                    if abs(row['utilization_percentage'] - overall_utilization) > 20:
                        direction = "under-utilization" if row['utilization_percentage'] < overall_utilization else "over-utilization"
                        st.write(f"- Address {direction} in {row['department']} ({row['utilization_percentage']}% vs {overall_utilization}% average)")
                
                # Download button
                if st.download_button(
                    label="Download Summary Report (CSV)",
                    data=summary_table.to_csv(index=False).encode('utf-8'),
                    file_name=f"resource_utilization_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Summary report downloaded successfully!")
        
        else:
            # Single department resource report
            department = selected_department if selected_department != "All Departments" else "Public Works"
            
            # Get resource data for this department
            resource_data = get_resource_data(department=department)
            
            if selected_format == "Interactive Dashboard":
                # Interactive dashboard view
                st.subheader(f"{department} Resource Utilization")
                
                # Resource allocation by category
                fig = px.pie(
                    resource_data,
                    values='allocation',
                    names='category',
                    title=f"Resource Allocation by Category",
                    color_discrete_sequence=px.colors.sequential.Blues
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Allocated vs spent by category
                fig2 = px.bar(
                    resource_data,
                    x='category',
                    y=['allocation', 'spent', 'remaining'],
                    title=f"Budget Allocation, Spent and Remaining by Category",
                    barmode='group',
                    labels={'value': 'Amount', 'variable': 'Category'}
                )
                st.plotly_chart(fig2, use_container_width=True)
                
                # Calculate utilization percentages
                resource_data['utilization_percentage'] = (resource_data['spent'] / resource_data['allocation'] * 100).round(1)
                
                # Utilization percentage chart
                fig3 = px.bar(
                    resource_data,
                    x='category',
                    y='utilization_percentage',
                    color='utilization_percentage',
                    color_continuous_scale='Greens',
                    title="Resource Utilization Percentage by Category",
                    labels={'utilization_percentage': 'Utilization %'}
                )
                st.plotly_chart(fig3, use_container_width=True)
                
                # Resource data table
                st.subheader("Resource Utilization Details")
                st.dataframe(resource_data, use_container_width=True)
                
                # Download button
                if st.download_button(
                    label="Download Resource Report (CSV)",
                    data=resource_data.to_csv(index=False).encode('utf-8'),
                    file_name=f"{department}_resource_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Report data downloaded successfully!")
            
            else:
                # Summary view
                st.subheader(f"{department} Resource Utilization Summary")
                
                # Calculate key metrics
                total_allocation = resource_data['allocation'].sum()
                total_spent = resource_data['spent'].sum()
                total_remaining = resource_data['remaining'].sum()
                overall_utilization = (total_spent / total_allocation * 100).round(1)
                
                # Calculate utilization percentages
                resource_data['utilization_percentage'] = (resource_data['spent'] / resource_data['allocation'] * 100).round(1)
                
                highest_category = resource_data.loc[resource_data['utilization_percentage'].idxmax()]
                lowest_category = resource_data.loc[resource_data['utilization_percentage'].idxmin()]
                
                # Display summary stats
                st.write(f"**Total Budget Allocation:** {format_number(total_allocation, is_currency=True)}")
                st.write(f"**Total Budget Spent:** {format_number(total_spent, is_currency=True)}")
                st.write(f"**Total Remaining Budget:** {format_number(total_remaining, is_currency=True)}")
                st.write(f"**Overall Utilization Rate:** {overall_utilization}%")
                st.write(f"**Category with Highest Utilization:** {highest_category['category']} ({highest_category['utilization_percentage']}%)")
                st.write(f"**Category with Lowest Utilization:** {lowest_category['category']} ({lowest_category['utilization_percentage']}%)")
                
                # Resource utilization table
                st.subheader("Resource Utilization by Category")
                
                # Create a summary table
                summary_table = resource_data[['category', 'allocation', 'spent', 'remaining', 'utilization_percentage']]
                summary_table = summary_table.sort_values('utilization_percentage', ascending=False)
                
                # Format currency columns
                summary_table['allocation'] = summary_table['allocation'].apply(lambda x: format_number(x, is_currency=True))
                summary_table['spent'] = summary_table['spent'].apply(lambda x: format_number(x, is_currency=True))
                summary_table['remaining'] = summary_table['remaining'].apply(lambda x: format_number(x, is_currency=True))
                summary_table['utilization_percentage'] = summary_table['utilization_percentage'].apply(lambda x: f"{x}%")
                
                st.dataframe(summary_table, use_container_width=True)
                
                # Recommendations
                st.subheader("Recommendations")
                
                if overall_utilization < 70:
                    st.write("- Review overall resource allocation to improve utilization rates")
                
                if lowest_category['utilization_percentage'] < 60:
                    st.write(f"- Evaluate {lowest_category['category']} budget to identify underutilized resources")
                
                if highest_category['utilization_percentage'] > 90:
                    st.write(f"- Consider increasing allocation for {highest_category['category']}")
                
                # Download button
                if st.download_button(
                    label="Download Summary Report (CSV)",
                    data=summary_table.to_csv(index=False).encode('utf-8'),
                    file_name=f"{department}_resource_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Summary report downloaded successfully!")
    
    elif selected_report == "Task Completion":
        # Task Completion Report
        if selected_department == "All Departments" and st.session_state.user_role == "administrator":
            # Get task data for all departments
            all_departments = ["Public Works", "Health Services", "Education", "Transportation", "Security"]
            all_tasks = pd.DataFrame()
            
            for dept in all_departments:
                dept_tasks = get_task_data(department=dept)
                all_tasks = pd.concat([all_tasks, dept_tasks])
            
            if selected_format == "Interactive Dashboard":
                # Interactive dashboard view
                st.subheader("District-wide Task Completion Analysis")
                
                # Task status distribution
                status_counts = all_tasks['status'].value_counts().reset_index()
                status_counts.columns = ['status', 'count']
                
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
                st.plotly_chart(fig, use_container_width=True)
                
                # Tasks by department
                dept_counts = all_tasks.groupby(['department', 'status']).size().reset_index(name='count')
                
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
                st.plotly_chart(fig2, use_container_width=True)
                
                # Tasks by priority
                priority_counts = all_tasks.groupby(['priority', 'status']).size().reset_index(name='count')
                
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
                st.plotly_chart(fig3, use_container_width=True)
                
                # Calculate overdue tasks
                all_tasks['due_date'] = pd.to_datetime(all_tasks['due_date'])
                today = pd.Timestamp(datetime.now().date())
                overdue_tasks = all_tasks[
                    (all_tasks['due_date'] < today) & 
                    (all_tasks['status'] != 'Completed')
                ]
                
                # Overdue tasks by department
                if not overdue_tasks.empty:
                    overdue_by_dept = overdue_tasks['department'].value_counts().reset_index()
                    overdue_by_dept.columns = ['department', 'count']
                    
                    fig4 = px.bar(
                        overdue_by_dept,
                        x='department',
                        y='count',
                        color='count',
                        title="Overdue Tasks by Department",
                        color_continuous_scale='Reds'
                    )
                    st.plotly_chart(fig4, use_container_width=True)
                
                # Task details
                st.subheader("Task Details")
                
                task_tabs = st.tabs(["All Tasks", "Overdue Tasks"])
                
                with task_tabs[0]:
                    st.dataframe(
                        all_tasks[['task_id', 'task_name', 'department', 'assigned_to', 'status', 'priority', 'due_date']],
                        use_container_width=True
                    )
                
                with task_tabs[1]:
                    if not overdue_tasks.empty:
                        st.dataframe(
                            overdue_tasks[['task_id', 'task_name', 'department', 'assigned_to', 'status', 'priority', 'due_date']],
                            use_container_width=True
                        )
                    else:
                        st.info("No overdue tasks found.")
                
                # Download button
                if st.download_button(
                    label="Download Task Report (CSV)",
                    data=all_tasks.to_csv(index=False).encode('utf-8'),
                    file_name=f"task_completion_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Report data downloaded successfully!")
            
            else:
                # Summary view
                st.subheader("Task Completion Summary")
                
                # Calculate key metrics
                total_tasks = len(all_tasks)
                completed_tasks = len(all_tasks[all_tasks['status'] == 'Completed'])
                in_progress_tasks = len(all_tasks[all_tasks['status'] == 'In Progress'])
                pending_tasks = len(all_tasks[all_tasks['status'] == 'Pending'])
                
                completion_rate = (completed_tasks / total_tasks * 100).round(1) if total_tasks > 0 else 0
                
                # Calculate overdue tasks
                all_tasks['due_date'] = pd.to_datetime(all_tasks['due_date'])
                today = pd.Timestamp(datetime.now().date())
                overdue_tasks = all_tasks[
                    (all_tasks['due_date'] < today) & 
                    (all_tasks['status'] != 'Completed')
                ]
                overdue_count = len(overdue_tasks)
                
                # Display summary stats
                st.write(f"**Total Tasks:** {total_tasks}")
                st.write(f"**Completed Tasks:** {completed_tasks} ({completion_rate}%)")
                st.write(f"**In Progress Tasks:** {in_progress_tasks}")
                st.write(f"**Pending Tasks:** {pending_tasks}")
                st.write(f"**Overdue Tasks:** {overdue_count}")
                
                # Department summary
                st.subheader("Department Task Summary")
                
                # Create department summary
                dept_summary = all_tasks.groupby('department')['status'].value_counts().unstack().fillna(0)
                
                # Calculate completion rates
                if 'Completed' in dept_summary.columns:
                    dept_summary['Total'] = dept_summary.sum(axis=1)
                    dept_summary['Completion Rate'] = (dept_summary['Completed'] / dept_summary['Total'] * 100).round(1)
                    
                    # Format the completion rate
                    dept_summary['Completion Rate'] = dept_summary['Completion Rate'].apply(lambda x: f"{x}%")
                    
                    # Convert to integers
                    for col in dept_summary.columns:
                        if col != 'Completion Rate':
                            dept_summary[col] = dept_summary[col].astype(int)
                    
                    st.dataframe(dept_summary, use_container_width=True)
                else:
                    st.info("No completed tasks found in the data.")
                
                # High-priority pending tasks
                high_priority_pending = all_tasks[
                    (all_tasks['status'] != 'Completed') & 
                    (all_tasks['priority'].isin(['High', 'Critical']))
                ]
                
                if not high_priority_pending.empty:
                    st.subheader("High Priority Pending Tasks")
                    st.dataframe(
                        high_priority_pending[['task_id', 'task_name', 'department', 'priority', 'due_date']],
                        use_container_width=True
                    )
                
                # Recommendations
                st.subheader("Recommendations")
                
                if overdue_count > 0:
                    st.write(f"- Address {overdue_count} overdue tasks across departments")
                
                if completion_rate < 70:
                    st.write("- Review task assignment and completion processes to improve efficiency")
                
                # Check departments with low completion rates
                if 'Completion Rate' in dept_summary.columns:
                    for dept, row in dept_summary.iterrows():
                        comp_rate = float(row['Completion Rate'].strip('%'))
                        if comp_rate < 60:
                            st.write(f"- Investigate low completion rate in {dept} department ({row['Completion Rate']})")
                
                # Download button
                if 'Completion Rate' in dept_summary.columns:
                    if st.download_button(
                        label="Download Summary Report (CSV)",
                        data=dept_summary.reset_index().to_csv(index=False).encode('utf-8'),
                        file_name=f"task_completion_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    ):
                        st.success("Summary report downloaded successfully!")
        
        else:
            # Single department task report
            department = selected_department if selected_department != "All Departments" else "Public Works"
            
            # Get task data for this department
            task_data = get_task_data(department=department)
            
            if selected_format == "Interactive Dashboard":
                # Interactive dashboard view
                st.subheader(f"{department} Task Completion Analysis")
                
                # Task status distribution
                status_counts = task_data['status'].value_counts().reset_index()
                status_counts.columns = ['status', 'count']
                
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
                st.plotly_chart(fig, use_container_width=True)
                
                # Tasks by assigned staff
                staff_counts = task_data.groupby(['assigned_to', 'status']).size().reset_index(name='count')
                
                fig2 = px.bar(
                    staff_counts,
                    x='assigned_to',
                    y='count',
                    color='status',
                    title="Tasks by Staff Member and Status",
                    color_discrete_map={
                        'Pending': '#FFC107',
                        'In Progress': '#2196F3',
                        'Completed': '#4CAF50'
                    }
                )
                st.plotly_chart(fig2, use_container_width=True)
                
                # Tasks by priority
                priority_counts = task_data.groupby(['priority', 'status']).size().reset_index(name='count')
                
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
                st.plotly_chart(fig3, use_container_width=True)
                
                # Calculate overdue tasks
                task_data['due_date'] = pd.to_datetime(task_data['due_date'])
                today = pd.Timestamp(datetime.now().date())
                overdue_tasks = task_data[
                    (task_data['due_date'] < today) & 
                    (task_data['status'] != 'Completed')
                ]
                
                # Task details
                st.subheader("Task Details")
                
                task_tabs = st.tabs(["All Tasks", "Overdue Tasks"])
                
                with task_tabs[0]:
                    st.dataframe(
                        task_data[['task_id', 'task_name', 'assigned_to', 'status', 'priority', 'due_date']],
                        use_container_width=True
                    )
                
                with task_tabs[1]:
                    if not overdue_tasks.empty:
                        st.dataframe(
                            overdue_tasks[['task_id', 'task_name', 'assigned_to', 'status', 'priority', 'due_date']],
                            use_container_width=True
                        )
                    else:
                        st.info("No overdue tasks found.")
                
                # Download button
                if st.download_button(
                    label="Download Task Report (CSV)",
                    data=task_data.to_csv(index=False).encode('utf-8'),
                    file_name=f"{department}_task_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Report data downloaded successfully!")
            
            else:
                # Summary view
                st.subheader(f"{department} Task Completion Summary")
                
                # Calculate key metrics
                total_tasks = len(task_data)
                completed_tasks = len(task_data[task_data['status'] == 'Completed'])
                in_progress_tasks = len(task_data[task_data['status'] == 'In Progress'])
                pending_tasks = len(task_data[task_data['status'] == 'Pending'])
                
                completion_rate = (completed_tasks / total_tasks * 100).round(1) if total_tasks > 0 else 0
                
                # Calculate overdue tasks
                task_data['due_date'] = pd.to_datetime(task_data['due_date'])
                today = pd.Timestamp(datetime.now().date())
                overdue_tasks = task_data[
                    (task_data['due_date'] < today) & 
                    (task_data['status'] != 'Completed')
                ]
                overdue_count = len(overdue_tasks)
                
                # Display summary stats
                st.write(f"**Total Tasks:** {total_tasks}")
                st.write(f"**Completed Tasks:** {completed_tasks} ({completion_rate}%)")
                st.write(f"**In Progress Tasks:** {in_progress_tasks}")
                st.write(f"**Pending Tasks:** {pending_tasks}")
                st.write(f"**Overdue Tasks:** {overdue_count}")
                
                # Staff summary
                st.subheader("Staff Task Summary")
                
                # Create staff summary
                staff_summary = task_data.groupby('assigned_to')['status'].value_counts().unstack().fillna(0)
                
                # Calculate completion rates
                if 'Completed' in staff_summary.columns:
                    staff_summary['Total'] = staff_summary.sum(axis=1)
                    staff_summary['Completion Rate'] = (staff_summary['Completed'] / staff_summary['Total'] * 100).round(1)
                    
                    # Format the completion rate
                    staff_summary['Completion Rate'] = staff_summary['Completion Rate'].apply(lambda x: f"{x}%")
                    
                    # Convert to integers
                    for col in staff_summary.columns:
                        if col != 'Completion Rate':
                            staff_summary[col] = staff_summary[col].astype(int)
                    
                    st.dataframe(staff_summary, use_container_width=True)
                else:
                    st.info("No completed tasks found in the data.")
                
                # High-priority pending tasks
                high_priority_pending = task_data[
                    (task_data['status'] != 'Completed') & 
                    (task_data['priority'].isin(['High', 'Critical']))
                ]
                
                if not high_priority_pending.empty:
                    st.subheader("High Priority Pending Tasks")
                    st.dataframe(
                        high_priority_pending[['task_id', 'task_name', 'assigned_to', 'priority', 'due_date']],
                        use_container_width=True
                    )
                
                # Recommendations
                st.subheader("Recommendations")
                
                if overdue_count > 0:
                    st.write(f"- Address {overdue_count} overdue tasks in the department")
                
                if completion_rate < 70:
                    st.write("- Review task assignment and completion processes to improve efficiency")
                
                # Check staff members with low completion rates
                if 'Completion Rate' in staff_summary.columns:
                    for staff, row in staff_summary.iterrows():
                        comp_rate = float(row['Completion Rate'].strip('%'))
                        if comp_rate < 60 and row['Total'] > 2:  # Only flag if more than 2 tasks assigned
                            st.write(f"- Investigate low completion rate for {staff} ({row['Completion Rate']})")
                
                # Download button
                if 'Completion Rate' in staff_summary.columns:
                    if st.download_button(
                        label="Download Summary Report (CSV)",
                        data=staff_summary.reset_index().to_csv(index=False).encode('utf-8'),
                        file_name=f"{department}_task_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    ):
                        st.success("Summary report downloaded successfully!")
    
    elif selected_report == "Citizen Satisfaction":
        # Citizen Satisfaction Report
        if selected_department == "All Departments" and st.session_state.user_role == "administrator":
            # Get satisfaction metrics for all departments
            all_departments = ["Public Works", "Health Services", "Education", "Transportation", "Security"]
            
            satisfaction_data = []
            for dept in all_departments:
                metrics = calculate_satisfaction_metrics(department=dept)
                
                # Convert historical data to a simple format
                hist_data = metrics['historical_data'].copy()
                hist_data['department'] = dept
                
                satisfaction_data.append({
                    'department': dept,
                    'current_score': metrics['current_score'],
                    'trend': metrics['trend'],
                    'historical_data': hist_data
                })
            
            if selected_format == "Interactive Dashboard":
                # Interactive dashboard view
                st.subheader("District-wide Citizen Satisfaction")
                
                # Create current satisfaction comparison
                current_scores = pd.DataFrame([
                    {'department': d['department'], 'satisfaction_score': d['current_score']}
                    for d in satisfaction_data
                ])
                
                fig = px.bar(
                    current_scores,
                    x='department',
                    y='satisfaction_score',
                    color='satisfaction_score',
                    color_continuous_scale='Blues',
                    title="Current Citizen Satisfaction by Department",
                    labels={'satisfaction_score': 'Satisfaction Score'}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Create historical trend visualization
                historical_df = pd.concat([d['historical_data'] for d in satisfaction_data])
                
                fig2 = px.line(
                    historical_df,
                    x='month',
                    y='satisfaction_score',
                    color='department',
                    title="Citizen Satisfaction Trends by Department",
                    labels={'satisfaction_score': 'Satisfaction Score'}
                )
                st.plotly_chart(fig2, use_container_width=True)
                
                # Satisfaction trends
                trends = pd.DataFrame([
                    {'department': d['department'], 'trend': d['trend']}
                    for d in satisfaction_data
                ])
                
                fig3 = px.bar(
                    trends,
                    x='department',
                    y='trend',
                    color='trend',
                    color_continuous_scale='RdBu',
                    title="Citizen Satisfaction Trends (% Change)",
                    labels={'trend': 'Trend (% Change)'}
                )
                fig3.update_layout(yaxis_zeroline=True)
                st.plotly_chart(fig3, use_container_width=True)
                
                # Satisfaction data table
                st.subheader("Satisfaction Metrics Details")
                
                # Create summary table
                summary_df = pd.DataFrame([
                    {
                        'department': d['department'], 
                        'current_score': d['current_score'],
                        'trend': d['trend'],
                        'previous_score': d['current_score'] - (d['current_score'] * d['trend'] / 100)
                    }
                    for d in satisfaction_data
                ])
                
                st.dataframe(summary_df, use_container_width=True)
                
                # Download button
                if st.download_button(
                    label="Download Satisfaction Report (CSV)",
                    data=summary_df.to_csv(index=False).encode('utf-8'),
                    file_name=f"citizen_satisfaction_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Report data downloaded successfully!")
            
            else:
                # Summary view
                st.subheader("Citizen Satisfaction Summary")
                
                # Create summary table
                summary_df = pd.DataFrame([
                    {
                        'department': d['department'], 
                        'current_score': d['current_score'],
                        'trend': d['trend'],
                        'previous_score': round(d['current_score'] - (d['current_score'] * d['trend'] / 100), 1)
                    }
                    for d in satisfaction_data
                ])
                
                # Calculate district average
                avg_satisfaction = summary_df['current_score'].mean()
                avg_trend = summary_df['trend'].mean()
                
                # Find highest and lowest satisfaction
                highest_dept = summary_df.loc[summary_df['current_score'].idxmax()]
                lowest_dept = summary_df.loc[summary_df['current_score'].idxmin()]
                
                # Display summary stats
                st.write(f"**District Average Satisfaction:** {avg_satisfaction:.1f}/100")
                st.write(f"**Average Trend:** {avg_trend:.1f}%")
                st.write(f"**Highest Satisfaction:** {highest_dept['department']} ({highest_dept['current_score']}/100)")
                st.write(f"**Lowest Satisfaction:** {lowest_dept['department']} ({lowest_dept['current_score']}/100)")
                
                # Display summary table
                st.subheader("Department Satisfaction Overview")
                
                # Format the trend column
                summary_df['trend'] = summary_df['trend'].apply(lambda x: f"{x:.1f}%")
                
                st.dataframe(summary_df, use_container_width=True)
                
                # Recommendations
                st.subheader("Recommendations")
                
                if avg_satisfaction < 75:
                    st.write("- Develop district-wide citizen satisfaction improvement plan")
                
                for _, row in summary_df.iterrows():
                    trend_val = float(row['trend'].strip('%'))
                    if trend_val < -5:
                        st.write(f"- Investigate declining satisfaction in {row['department']} (trend: {row['trend']})")
                
                if lowest_dept['current_score'] < 70:
                    st.write(f"- Create targeted improvement plan for {lowest_dept['department']}")
                
                if highest_dept['current_score'] > 90:
                    st.write(f"- Identify and replicate best practices from {highest_dept['department']}")
                
                # Download button
                if st.download_button(
                    label="Download Summary Report (CSV)",
                    data=summary_df.to_csv(index=False).encode('utf-8'),
                    file_name=f"satisfaction_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Summary report downloaded successfully!")
        
        else:
            # Single department satisfaction report
            department = selected_department if selected_department != "All Departments" else "Public Works"
            
            # Get satisfaction metrics for this department
            metrics = calculate_satisfaction_metrics(department=department)
            
            if selected_format == "Interactive Dashboard":
                # Interactive dashboard view
                st.subheader(f"{department} Citizen Satisfaction Analysis")
                
                # Current satisfaction score
                st.metric(
                    "Current Satisfaction Score", 
                    f"{metrics['current_score']}/100", 
                    f"{metrics['trend']}%"
                )
                
                # Historical trend visualization
                historical_df = metrics['historical_data']
                
                fig = px.line(
                    historical_df,
                    x='month',
                    y='satisfaction_score',
                    title=f"{department} Satisfaction Trend",
                    labels={'satisfaction_score': 'Satisfaction Score'}
                )
                fig.update_layout(yaxis_range=[
                    max(0, historical_df['satisfaction_score'].min() - 10),
                    min(100, historical_df['satisfaction_score'].max() + 10)
                ])
                st.plotly_chart(fig, use_container_width=True)
                
                # Monthly comparison
                fig2 = px.bar(
                    historical_df,
                    x='month',
                    y='satisfaction_score',
                    title="Monthly Satisfaction Scores",
                    color='satisfaction_score',
                    color_continuous_scale='Blues',
                    labels={'satisfaction_score': 'Satisfaction Score'}
                )
                st.plotly_chart(fig2, use_container_width=True)
                
                # Department comparison with district average
                # Get district average
                all_departments = ["Public Works", "Health Services", "Education", "Transportation", "Security"]
                
                district_avg = []
                for month in historical_df['month'].unique():
                    month_scores = []
                    for dept in all_departments:
                        if dept != department:
                            other_metrics = calculate_satisfaction_metrics(department=dept)
                            other_df = other_metrics['historical_data']
                            if month in other_df['month'].values:
                                month_score = other_df.loc[other_df['month'] == month, 'satisfaction_score'].iloc[0]
                                month_scores.append(month_score)
                    
                    if month_scores:
                        district_avg.append({
                            'month': month,
                            'satisfaction_score': np.mean(month_scores),
                            'source': 'District Average'
                        })
                
                if district_avg:
                    # Add source column to historical data
                    historical_df['source'] = department
                    
                    # Create combined dataframe
                    district_avg_df = pd.DataFrame(district_avg)
                    combined_df = pd.concat([historical_df, district_avg_df])
                    
                    # Create comparison chart
                    fig3 = px.line(
                        combined_df,
                        x='month',
                        y='satisfaction_score',
                        color='source',
                        title=f"{department} vs District Average",
                        labels={'satisfaction_score': 'Satisfaction Score'}
                    )
                    st.plotly_chart(fig3, use_container_width=True)
                
                # Download button
                if st.download_button(
                    label="Download Satisfaction Report (CSV)",
                    data=historical_df.to_csv(index=False).encode('utf-8'),
                    file_name=f"{department}_satisfaction_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Report data downloaded successfully!")
            
            else:
                # Summary view
                st.subheader(f"{department} Citizen Satisfaction Summary")
                
                # Display current metrics
                st.write(f"**Current Satisfaction Score:** {metrics['current_score']}/100")
                st.write(f"**Trend:** {metrics['trend']}%")
                
                # Calculate previous score
                previous_score = round(metrics['current_score'] - (metrics['current_score'] * metrics['trend'] / 100), 1)
                st.write(f"**Previous Score:** {previous_score}/100")
                
                # Display historical data
                st.subheader("Monthly Satisfaction Scores")
                
                # Historical data table
                historical_df = metrics['historical_data']
                st.dataframe(historical_df, use_container_width=True)
                
                # Performance assessment
                st.subheader("Performance Assessment")
                
                if metrics['current_score'] >= 90:
                    assessment = "Excellent"
                    color = "green"
                elif metrics['current_score'] >= 80:
                    assessment = "Good"
                    color = "blue"
                elif metrics['current_score'] >= 70:
                    assessment = "Satisfactory"
                    color = "orange"
                else:
                    assessment = "Needs Improvement"
                    color = "red"
                
                st.markdown(f"<p style='color:{color};font-size:18px;'><strong>Assessment:</strong> {assessment}</p>", unsafe_allow_html=True)
                
                # Recommendations
                st.subheader("Recommendations")
                
                if metrics['trend'] < -5:
                    st.write("- Investigate causes for declining satisfaction scores")
                
                if metrics['current_score'] < 75:
                    st.write("- Develop targeted improvement plan for citizen satisfaction")
                
                # Check satisfaction trend over time
                hist_scores = historical_df['satisfaction_score'].tolist()
                if len(hist_scores) > 2 and all(hist_scores[i] <= hist_scores[i+1] for i in range(len(hist_scores)-2)):
                    st.write("- Continue successful initiatives that are driving consistent improvement")
                elif len(hist_scores) > 2 and all(hist_scores[i] >= hist_scores[i+1] for i in range(len(hist_scores)-2)):
                    st.write("- Address consistent decline in satisfaction scores with immediate action plan")
                
                # Download button
                if st.download_button(
                    label="Download Summary Report (CSV)",
                    data=historical_df.to_csv(index=False).encode('utf-8'),
                    file_name=f"{department}_satisfaction_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Summary report downloaded successfully!")
    
    elif selected_report == "Budget Analysis":
        # Budget Analysis Report
        if selected_department == "All Departments" and st.session_state.user_role == "administrator":
            # Get budget data for all departments
            resource_data = get_resource_data(all_departments=True)
            
            if selected_format == "Interactive Dashboard":
                # Interactive dashboard view
                st.subheader("District-wide Budget Analysis")
                
                # Budget allocation chart
                fig = px.pie(
                    resource_data,
                    values='budget_allocation',
                    names='department',
                    title="Budget Allocation by Department",
                    hole=0.4
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                # Budget vs spent comparison
                fig2 = px.bar(
                    resource_data,
                    x='department',
                    y=['budget_allocation', 'budget_spent'],
                    title="Budget Allocation vs Spent by Department",
                    barmode='group',
                    labels={'value': 'Amount', 'variable': 'Category'}
                )
                st.plotly_chart(fig2, use_container_width=True)
                
                # Calculate utilization and remaining budget
                resource_data['utilization_percentage'] = (resource_data['budget_spent'] / resource_data['budget_allocation'] * 100).round(1)
                resource_data['remaining_budget'] = resource_data['budget_allocation'] - resource_data['budget_spent']
                
                # Utilization percentage chart
                fig3 = px.bar(
                    resource_data,
                    x='department',
                    y='utilization_percentage',
                    color='utilization_percentage',
                    color_continuous_scale='Greens',
                    title="Budget Utilization Percentage by Department",
                    labels={'utilization_percentage': 'Utilization %'}
                )
                st.plotly_chart(fig3, use_container_width=True)
                
                # Remaining budget chart
                fig4 = px.bar(
                    resource_data,
                    x='department',
                    y='remaining_budget',
                    color='remaining_budget',
                    color_continuous_scale='Blues',
                    title="Remaining Budget by Department",
                    labels={'remaining_budget': 'Remaining Budget'}
                )
                st.plotly_chart(fig4, use_container_width=True)
                
                # Budget data table
                st.subheader("Budget Details")
                display_df = resource_data[['department', 'budget_allocation', 'budget_spent', 'remaining_budget', 'utilization_percentage']]
                display_df = display_df.sort_values('budget_allocation', ascending=False)
                st.dataframe(display_df, use_container_width=True)
                
                # Total budget metrics
                total_budget = resource_data['budget_allocation'].sum()
                total_spent = resource_data['budget_spent'].sum()
                total_remaining = total_budget - total_spent
                overall_utilization = (total_spent / total_budget * 100).round(1) if total_budget > 0 else 0
                
                # Display totals
                st.subheader("Budget Summary")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Budget", f"${total_budget:,.2f}")
                
                with col2:
                    st.metric("Total Spent", f"${total_spent:,.2f}")
                
                with col3:
                    st.metric("Total Remaining", f"${total_remaining:,.2f}")
                
                with col4:
                    st.metric("Overall Utilization", f"{overall_utilization}%")
                
                # Download button
                if st.download_button(
                    label="Download Budget Report (CSV)",
                    data=display_df.to_csv(index=False).encode('utf-8'),
                    file_name=f"budget_analysis_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Report data downloaded successfully!")
            
            else:
                # Summary view
                st.subheader("Budget Analysis Summary")
                
                # Calculate utilization and remaining budget
                resource_data['utilization_percentage'] = (resource_data['budget_spent'] / resource_data['budget_allocation'] * 100).round(1)
                resource_data['remaining_budget'] = resource_data['budget_allocation'] - resource_data['budget_spent']
                
                # Calculate totals
                total_budget = resource_data['budget_allocation'].sum()
                total_spent = resource_data['budget_spent'].sum()
                total_remaining = total_budget - total_spent
                overall_utilization = (total_spent / total_budget * 100).round(1) if total_budget > 0 else 0
                
                # Identify highest and lowest utilization
                highest_util = resource_data.loc[resource_data['utilization_percentage'].idxmax()]
                lowest_util = resource_data.loc[resource_data['utilization_percentage'].idxmin()]
                
                # Display summary stats
                st.write(f"**Total Budget:** {format_number(total_budget, is_currency=True)}")
                st.write(f"**Total Spent:** {format_number(total_spent, is_currency=True)} ({overall_utilization}% utilization)")
                st.write(f"**Total Remaining:** {format_number(total_remaining, is_currency=True)}")
                st.write(f"**Highest Utilization:** {highest_util['department']} ({highest_util['utilization_percentage']}%)")
                st.write(f"**Lowest Utilization:** {lowest_util['department']} ({lowest_util['utilization_percentage']}%)")
                
                # Department budget table
                st.subheader("Department Budget Overview")
                
                # Create a summary table
                summary_df = resource_data[['department', 'budget_allocation', 'budget_spent', 'remaining_budget', 'utilization_percentage']]
                summary_df = summary_df.sort_values('budget_allocation', ascending=False)
                
                # Format currency columns
                display_df = summary_df.copy()
                display_df['budget_allocation'] = display_df['budget_allocation'].apply(lambda x: format_number(x, is_currency=True))
                display_df['budget_spent'] = display_df['budget_spent'].apply(lambda x: format_number(x, is_currency=True))
                display_df['remaining_budget'] = display_df['remaining_budget'].apply(lambda x: format_number(x, is_currency=True))
                display_df['utilization_percentage'] = display_df['utilization_percentage'].apply(lambda x: f"{x}%")
                
                st.dataframe(display_df, use_container_width=True)
                
                # Budget utilization assessment
                st.subheader("Budget Utilization Assessment")
                
                # Count departments in different utilization categories
                under_utilized = len(summary_df[summary_df['utilization_percentage'] < 65])
                optimal_utilized = len(summary_df[(summary_df['utilization_percentage'] >= 65) & (summary_df['utilization_percentage'] <= 85)])
                over_utilized = len(summary_df[summary_df['utilization_percentage'] > 85])
                
                st.write(f"**Under-utilized departments (< 65%):** {under_utilized}")
                st.write(f"**Optimally utilized departments (65-85%):** {optimal_utilized}")
                st.write(f"**Over-utilized departments (> 85%):** {over_utilized}")
                
                # Recommendations
                st.subheader("Recommendations")
                
                if overall_utilization < 65:
                    st.write("- Review overall budget allocation to improve utilization rates")
                
                if under_utilized > 0:
                    st.write(f"- Evaluate budget allocation for {under_utilized} under-utilized departments")
                
                if over_utilized > 0:
                    st.write(f"- Consider additional resources for {over_utilized} over-utilized departments")
                
                # List specific recommendations for outliers
                for _, row in summary_df.iterrows():
                    if row['utilization_percentage'] < 50:
                        st.write(f"- Significant under-utilization in {row['department']} ({row['utilization_percentage']}%) - consider reallocating resources")
                    elif row['utilization_percentage'] > 95:
                        st.write(f"- {row['department']} is at risk of budget shortfall ({row['utilization_percentage']}%) - review resource needs")
                
                # Download button
                if st.download_button(
                    label="Download Summary Report (CSV)",
                    data=summary_df.to_csv(index=False).encode('utf-8'),
                    file_name=f"budget_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Summary report downloaded successfully!")
        
        else:
            # Single department budget report
            department = selected_department if selected_department != "All Departments" else "Public Works"
            
            # Get budget data for this department
            resource_data = get_resource_data(department=department)
            
            if selected_format == "Interactive Dashboard":
                # Interactive dashboard view
                st.subheader(f"{department} Budget Analysis")
                
                # Budget allocation by category
                fig = px.pie(
                    resource_data,
                    values='allocation',
                    names='category',
                    title=f"Budget Allocation by Category",
                    color_discrete_sequence=px.colors.sequential.Blues
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Budget vs spent by category
                fig2 = px.bar(
                    resource_data,
                    x='category',
                    y=['allocation', 'spent', 'remaining'],
                    title=f"Budget Allocation, Spent and Remaining by Category",
                    barmode='group',
                    labels={'value': 'Amount', 'variable': 'Category'}
                )
                st.plotly_chart(fig2, use_container_width=True)
                
                # Calculate utilization percentages
                resource_data['utilization_percentage'] = (resource_data['spent'] / resource_data['allocation'] * 100).round(1)
                
                # Utilization percentage chart
                fig3 = px.bar(
                    resource_data,
                    x='category',
                    y='utilization_percentage',
                    color='utilization_percentage',
                    color_continuous_scale='Greens',
                    title="Budget Utilization Percentage by Category",
                    labels={'utilization_percentage': 'Utilization %'}
                )
                st.plotly_chart(fig3, use_container_width=True)
                
                # Budget data table
                st.subheader("Budget Details by Category")
                st.dataframe(resource_data, use_container_width=True)
                
                # Total budget metrics
                total_allocation = resource_data['allocation'].sum()
                total_spent = resource_data['spent'].sum()
                total_remaining = resource_data['remaining'].sum()
                overall_utilization = (total_spent / total_allocation * 100).round(1) if total_allocation > 0 else 0
                
                # Display totals
                st.subheader("Budget Summary")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Budget", f"${total_allocation:,.2f}")
                
                with col2:
                    st.metric("Total Spent", f"${total_spent:,.2f}")
                
                with col3:
                    st.metric("Total Remaining", f"${total_remaining:,.2f}")
                
                with col4:
                    st.metric("Overall Utilization", f"{overall_utilization}%")
                
                # Download button
                if st.download_button(
                    label="Download Budget Report (CSV)",
                    data=resource_data.to_csv(index=False).encode('utf-8'),
                    file_name=f"{department}_budget_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Report data downloaded successfully!")
            
            else:
                # Summary view
                st.subheader(f"{department} Budget Analysis Summary")
                
                # Calculate utilization percentages
                resource_data['utilization_percentage'] = (resource_data['spent'] / resource_data['allocation'] * 100).round(1)
                
                # Calculate totals
                total_allocation = resource_data['allocation'].sum()
                total_spent = resource_data['spent'].sum()
                total_remaining = resource_data['remaining'].sum()
                overall_utilization = (total_spent / total_allocation * 100).round(1) if total_allocation > 0 else 0
                
                # Identify highest and lowest utilization categories
                highest_util = resource_data.loc[resource_data['utilization_percentage'].idxmax()]
                lowest_util = resource_data.loc[resource_data['utilization_percentage'].idxmin()]
                
                # Display summary stats
                st.write(f"**Total Budget:** {format_number(total_allocation, is_currency=True)}")
                st.write(f"**Total Spent:** {format_number(total_spent, is_currency=True)} ({overall_utilization}% utilization)")
                st.write(f"**Total Remaining:** {format_number(total_remaining, is_currency=True)}")
                st.write(f"**Highest Utilization Category:** {highest_util['category']} ({highest_util['utilization_percentage']}%)")
                st.write(f"**Lowest Utilization Category:** {lowest_util['category']} ({lowest_util['utilization_percentage']}%)")
                
                # Category budget table
                st.subheader("Budget Overview by Category")
                
                # Create a summary table
                summary_df = resource_data[['category', 'allocation', 'spent', 'remaining', 'utilization_percentage']]
                summary_df = summary_df.sort_values('allocation', ascending=False)
                
                # Format currency columns
                display_df = summary_df.copy()
                display_df['allocation'] = display_df['allocation'].apply(lambda x: format_number(x, is_currency=True))
                display_df['spent'] = display_df['spent'].apply(lambda x: format_number(x, is_currency=True))
                display_df['remaining'] = display_df['remaining'].apply(lambda x: format_number(x, is_currency=True))
                display_df['utilization_percentage'] = display_df['utilization_percentage'].apply(lambda x: f"{x}%")
                
                st.dataframe(display_df, use_container_width=True)
                
                # Budget utilization assessment
                st.subheader("Budget Utilization Assessment")
                
                # Count categories in different utilization bands
                under_utilized = len(summary_df[summary_df['utilization_percentage'] < 65])
                optimal_utilized = len(summary_df[(summary_df['utilization_percentage'] >= 65) & (summary_df['utilization_percentage'] <= 85)])
                over_utilized = len(summary_df[summary_df['utilization_percentage'] > 85])
                
                st.write(f"**Under-utilized categories (< 65%):** {under_utilized}")
                st.write(f"**Optimally utilized categories (65-85%):** {optimal_utilized}")
                st.write(f"**Over-utilized categories (> 85%):** {over_utilized}")
                
                # Recommendations
                st.subheader("Recommendations")
                
                if overall_utilization < 65:
                    st.write("- Review overall department budget allocation to improve utilization")
                
                if under_utilized > 0:
                    st.write(f"- Evaluate resource allocation for {under_utilized} under-utilized budget categories")
                
                if over_utilized > 0:
                    st.write(f"- Consider additional resources for {over_utilized} over-utilized budget categories")
                
                # List specific recommendations for outliers
                for _, row in summary_df.iterrows():
                    if row['utilization_percentage'] < 50:
                        st.write(f"- Significant under-utilization in {row['category']} category ({row['utilization_percentage']}%) - consider reallocating resources")
                    elif row['utilization_percentage'] > 95:
                        st.write(f"- {row['category']} category is at risk of budget shortfall ({row['utilization_percentage']}%) - review resource needs")
                
                # Download button
                if st.download_button(
                    label="Download Summary Report (CSV)",
                    data=summary_df.to_csv(index=False).encode('utf-8'),
                    file_name=f"{department}_budget_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                ):
                    st.success("Summary report downloaded successfully!")
    
    elif selected_report == "Cross-Department Comparison":
        # Cross-Department Comparison Report (only for administrators)
        if st.session_state.user_role != "administrator":
            st.warning("Cross-Department Comparison reports are only available to administrators.")
            st.stop()
        
        # Get comparison data for all departments
        comparison_data = calculate_department_comparison()
        
        if selected_format == "Interactive Dashboard":
            # Interactive dashboard view
            st.subheader("Cross-Department Comparison Analysis")
            
            # Performance metrics comparison
            metrics_tab, resources_tab, satisfaction_tab, tasks_tab = st.tabs([
                "Performance Metrics", 
                "Resource Utilization", 
                "Citizen Satisfaction",
                "Task Management"
            ])
            
            with metrics_tab:
                # Performance score comparison
                fig = px.bar(
                    comparison_data,
                    x='department',
                    y='performance_score',
                    color='performance_score',
                    color_continuous_scale='Blues',
                    title="Performance Score by Department"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Get detailed performance data
                all_departments = ["Public Works", "Health Services", "Education", "Transportation", "Security"]
                performance_data = pd.DataFrame()
                
                for dept in all_departments:
                    dept_data = get_performance_data(department=dept)
                    performance_data = pd.concat([performance_data, dept_data])
                
                # Performance trend chart
                if 'month' in performance_data.columns and 'efficiency_score' in performance_data.columns:
                    fig2 = px.line(
                        performance_data,
                        x='month',
                        y='efficiency_score',
                        color='department',
                        title="Performance Trend by Department",
                        labels={'efficiency_score': 'Efficiency Score'}
                    )
                    st.plotly_chart(fig2, use_container_width=True)
            
            with resources_tab:
                # Resource efficiency comparison
                fig3 = px.bar(
                    comparison_data,
                    x='department',
                    y='resource_efficiency',
                    color='resource_efficiency',
                    color_continuous_scale='Greens',
                    title="Resource Efficiency by Department"
                )
                st.plotly_chart(fig3, use_container_width=True)
                
                # Get detailed resource data
                resource_data = get_resource_data(all_departments=True)
                
                # Calculate utilization percentages
                resource_data['utilization_percentage'] = (resource_data['budget_spent'] / resource_data['budget_allocation'] * 100).round(1)
                
                # Budget allocation comparison
                fig4 = px.pie(
                    resource_data,
                    values='budget_allocation',
                    names='department',
                    title="Budget Allocation by Department",
                    hole=0.4
                )
                st.plotly_chart(fig4, use_container_width=True)
                
                # Utilization percentage comparison
                fig5 = px.bar(
                    resource_data,
                    x='department',
                    y='utilization_percentage',
                    color='utilization_percentage',
                    color_continuous_scale='RdYlGn',
                    title="Budget Utilization Percentage by Department",
                    labels={'utilization_percentage': 'Utilization %'}
                )
                st.plotly_chart(fig5, use_container_width=True)
            
            with satisfaction_tab:
                # Satisfaction score comparison
                fig6 = px.bar(
                    comparison_data,
                    x='department',
                    y='satisfaction_score',
                    color='satisfaction_score',
                    color_continuous_scale='Blues',
                    title="Citizen Satisfaction Score by Department"
                )
                st.plotly_chart(fig6, use_container_width=True)
                
                # Get detailed satisfaction data
                all_departments = ["Public Works", "Health Services", "Education", "Transportation", "Security"]
                
                historical_data = []
                for dept in all_departments:
                    metrics = calculate_satisfaction_metrics(department=dept)
                    dept_data = metrics['historical_data']
                    dept_data['department'] = dept
                    historical_data.append(dept_data)
                
                if historical_data:
                    historical_df = pd.concat(historical_data)
                    
                    # Satisfaction trend chart
                    fig7 = px.line(
                        historical_df,
                        x='month',
                        y='satisfaction_score',
                        color='department',
                        title="Satisfaction Trend by Department",
                        labels={'satisfaction_score': 'Satisfaction Score'}
                    )
                    st.plotly_chart(fig7, use_container_width=True)
            
            with tasks_tab:
                # Get task data for all departments
                all_departments = ["Public Works", "Health Services", "Education", "Transportation", "Security"]
                task_data = pd.DataFrame()
                
                for dept in all_departments:
                    dept_tasks = get_task_data(department=dept)
                    task_data = pd.concat([task_data, dept_tasks])
                
                # Task status distribution by department
                dept_status = task_data.groupby(['department', 'status']).size().reset_index(name='count')
                
                fig8 = px.bar(
                    dept_status,
                    x='department',
                    y='count',
                    color='status',
                    title="Task Status Distribution by Department",
                    color_discrete_map={
                        'Pending': '#FFC107',
                        'In Progress': '#2196F3',
                        'Completed': '#4CAF50'
                    }
                )
                st.plotly_chart(fig8, use_container_width=True)
                
                # Calculate completion rates
                completion_data = []
                for dept in all_departments:
                    dept_tasks = task_data[task_data['department'] == dept]
                    total = len(dept_tasks)
                    completed = len(dept_tasks[dept_tasks['status'] == 'Completed'])
                    rate = (completed / total * 100) if total > 0 else 0
                    
                    completion_data.append({
                        'department': dept,
                        'completion_rate': round(rate, 1)
                    })
                
                completion_df = pd.DataFrame(completion_data)
                
                # Task completion rate comparison
                fig9 = px.bar(
                    completion_df,
                    x='department',
                    y='completion_rate',
                    color='completion_rate',
                    color_continuous_scale='Greens',
                    title="Task Completion Rate by Department",
                    labels={'completion_rate': 'Completion Rate (%)'}
                )
                st.plotly_chart(fig9, use_container_width=True)
            
            # Overall department ranking
            st.subheader("Department Performance Ranking")
            
            # Create ranking based on multiple metrics
            ranking_data = comparison_data.copy()
            
            # Calculate completion rates and add to ranking
            if 'completion_df' in locals():
                ranking_data = pd.merge(ranking_data, completion_df, on='department')
            
            # Add resource utilization if available
            if 'resource_data' in locals() and 'utilization_percentage' in resource_data.columns:
                util_data = resource_data[['department', 'utilization_percentage']]
                ranking_data = pd.merge(ranking_data, util_data, on='department')
            
            # Calculate overall score (weighted average of metrics)
            if 'completion_rate' in ranking_data.columns and 'utilization_percentage' in ranking_data.columns:
                ranking_data['overall_score'] = (
                    ranking_data['performance_score'] * 0.35 +
                    ranking_data['satisfaction_score'] * 0.25 +
                    ranking_data['resource_efficiency'] * 0.2 +
                    ranking_data['completion_rate'] * 0.1 +
                    ranking_data['utilization_percentage'] * 0.1
                ).round(1)
                
                # Sort by overall score
                ranking_data = ranking_data.sort_values('overall_score', ascending=False)
                ranking_data['rank'] = range(1, len(ranking_data) + 1)
                
                # Display ranking table
                display_cols = ['rank', 'department', 'overall_score', 'performance_score', 
                                'satisfaction_score', 'resource_efficiency', 
                                'completion_rate', 'utilization_percentage']
                
                st.dataframe(ranking_data[display_cols], use_container_width=True)
            else:
                # Fallback to simpler ranking if data is missing
                ranking_data['overall_score'] = (
                    ranking_data['performance_score'] * 0.5 +
                    ranking_data['satisfaction_score'] * 0.3 +
                    ranking_data['resource_efficiency'] * 0.2
                ).round(1)
                
                # Sort by overall score
                ranking_data = ranking_data.sort_values('overall_score', ascending=False)
                ranking_data['rank'] = range(1, len(ranking_data) + 1)
                
                # Display ranking table
                display_cols = ['rank', 'department', 'overall_score', 'performance_score', 
                                'satisfaction_score', 'resource_efficiency']
                
                st.dataframe(ranking_data[display_cols], use_container_width=True)
            
            # Download button
            if st.download_button(
                label="Download Comparison Report (CSV)",
                data=ranking_data.to_csv(index=False).encode('utf-8'),
                file_name=f"department_comparison_report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            ):
                st.success("Report data downloaded successfully!")
        
        else:
            # Summary view
            st.subheader("Cross-Department Comparison Summary")
            
            # Get resource utilization data
            resource_data = get_resource_data(all_departments=True)
            resource_data['utilization_percentage'] = (resource_data['budget_spent'] / resource_data['budget_allocation'] * 100).round(1)
            
            # Get task completion data
            all_departments = ["Public Works", "Health Services", "Education", "Transportation", "Security"]
            task_data = pd.DataFrame()
            
            for dept in all_departments:
                dept_tasks = get_task_data(department=dept)
                task_data = pd.concat([task_data, dept_tasks])
            
            # Calculate completion rates
            completion_data = []
            for dept in all_departments:
                dept_tasks = task_data[task_data['department'] == dept]
                total = len(dept_tasks)
                completed = len(dept_tasks[dept_tasks['status'] == 'Completed'])
                rate = (completed / total * 100) if total > 0 else 0
                
                completion_data.append({
                    'department': dept,
                    'completion_rate': round(rate, 1)
                })
            
            completion_df = pd.DataFrame(completion_data)
            
            # Combine all metrics
            comparison_summary = comparison_data.copy()
            
            # Add resource utilization
            util_data = resource_data[['department', 'utilization_percentage']]
            comparison_summary = pd.merge(comparison_summary, util_data, on='department')
            
            # Add completion rate
            comparison_summary = pd.merge(comparison_summary, completion_df, on='department')
            
            # Calculate overall score
            comparison_summary['overall_score'] = (
                comparison_summary['performance_score'] * 0.35 +
                comparison_summary['satisfaction_score'] * 0.25 +
                comparison_summary['resource_efficiency'] * 0.2 +
                comparison_summary['completion_rate'] * 0.1 +
                comparison_summary['utilization_percentage'] * 0.1
            ).round(1)
            
            # Sort by overall score
            comparison_summary = comparison_summary.sort_values('overall_score', ascending=False)
            comparison_summary['rank'] = range(1, len(comparison_summary) + 1)
            
            # Display top performer
            top_dept = comparison_summary.iloc[0]
            bottom_dept = comparison_summary.iloc[-1]
            
            st.write("### Top Performing Department")
            st.write(f"**{top_dept['department']}** (Overall Score: {top_dept['overall_score']})")
            st.write(f"- Performance Score: {top_dept['performance_score']}")
            st.write(f"- Satisfaction Score: {top_dept['satisfaction_score']}")
            st.write(f"- Resource Efficiency: {top_dept['resource_efficiency']}")
            st.write(f"- Task Completion Rate: {top_dept['completion_rate']}%")
            st.write(f"- Budget Utilization: {top_dept['utilization_percentage']}%")
            
            # Department comparison table
            st.write("### Department Rankings")
            
            # Format the display table
            display_df = comparison_summary.copy()
            display_df['completion_rate'] = display_df['completion_rate'].apply(lambda x: f"{x}%")
            display_df['utilization_percentage'] = display_df['utilization_percentage'].apply(lambda x: f"{x}%")
            
            st.dataframe(display_df[['rank', 'department', 'overall_score', 'performance_score', 
                                   'satisfaction_score', 'resource_efficiency', 
                                   'completion_rate', 'utilization_percentage']], use_container_width=True)
            
            # Comparative analysis
            st.write("### Comparative Analysis")
            
            # Performance gaps
            performance_gap = top_dept['performance_score'] - bottom_dept['performance_score']
            satisfaction_gap = top_dept['satisfaction_score'] - bottom_dept['satisfaction_score']
            
            st.write(f"**Performance Gap:** {performance_gap:.1f} points between top and bottom departments")
            st.write(f"**Satisfaction Gap:** {satisfaction_gap:.1f} points between top and bottom departments")
            
            # Department strengths and weaknesses
            st.write("### Department Strengths and Areas for Improvement")
            
            for _, dept in comparison_summary.iterrows():
                with st.expander(f"{dept['department']} (Rank: {dept['rank']})"):
                    # Determine strengths (top 2 metrics)
                    metrics = {
                        'Performance': dept['performance_score'],
                        'Satisfaction': dept['satisfaction_score'],
                        'Resource Efficiency': dept['resource_efficiency'],
                        'Task Completion': dept['completion_rate'],
                        'Budget Utilization': dept['utilization_percentage']
                    }
                    
                    sorted_metrics = sorted(metrics.items(), key=lambda x: x[1], reverse=True)
                    strengths = sorted_metrics[:2]
                    weaknesses = sorted_metrics[-2:]
                    
                    st.write("**Strengths:**")
                    for metric, value in strengths:
                        formatted_value = f"{value}%" if metric in ['Task Completion', 'Budget Utilization'] else value
                        st.write(f"- {metric}: {formatted_value}")
                    
                    st.write("**Areas for Improvement:**")
                    for metric, value in weaknesses:
                        formatted_value = f"{value}%" if metric in ['Task Completion', 'Budget Utilization'] else value
                        st.write(f"- {metric}: {formatted_value}")
            
            # Recommendations
            st.write("### Key Recommendations")
            
            # Overall recommendations
            st.write("**District-wide Recommendations:**")
            st.write("1. Implement best practices from top-performing departments across the district")
            st.write("2. Focus on closing performance and satisfaction gaps between departments")
            st.write("3. Establish regular cross-department coordination for resource sharing and knowledge transfer")
            
            # Department-specific recommendations
            st.write("**Department-Specific Recommendations:**")
            
            for _, dept in comparison_summary.iterrows():
                if dept['performance_score'] < 70:
                    st.write(f"- Develop performance improvement plan for {dept['department']}")
                
                if dept['utilization_percentage'] < 65:
                    st.write(f"- Review budget allocation for {dept['department']} to improve utilization")
                
                if dept['completion_rate'] < 60:
                    st.write(f"- Implement task management improvements for {dept['department']}")
            
            # Download button
            if st.download_button(
                label="Download Comparison Summary (CSV)",
                data=comparison_summary.to_csv(index=False).encode('utf-8'),
                file_name=f"department_comparison_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            ):
                st.success("Summary report downloaded successfully!")
    
    else:
        # Fall back to a basic report if type not recognized
        st.info("Please select a report type from the sidebar to generate a report.")

# Add report export options in sidebar
with st.sidebar:
    st.markdown("---")
    st.subheader("Export Options")
    
    export_format = st.selectbox("Export Format", ["CSV", "PDF", "Excel"])
    
    if st.button("Export Full Report"):
        if export_format == "CSV":
            st.success("In a production environment, this would export a full CSV report.")
        elif export_format == "PDF":
            st.success("In a production environment, this would export a PDF report.")
        else:
            st.success("In a production environment, this would export an Excel report.")
