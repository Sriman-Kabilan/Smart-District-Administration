import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_handler import get_department_data, get_task_data

# Configure page
st.set_page_config(
    page_title="Department Coordination - District Admin",
    page_icon="🔄",
    layout="wide"
)

# Authentication check
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to access this page")
    st.stop()

# Page title
st.title("🔄 Department Coordination")
st.write("Coordinate activities and resources across departments")

# Only show to administrators or department heads
if st.session_state.user_role not in ["administrator", "department_head"]:
    st.warning("You do not have permission to view this page.")
    st.info("This page is only accessible to administrators and department heads.")
    st.stop()

# Sidebar for filtering
with st.sidebar:
    st.header("Coordination Options")
    
    # Department selection
    if st.session_state.user_role == "administrator":
        departments = ["All Departments", "Public Works", "Health Services", "Education", "Transportation", "Security"]
        primary_department = st.selectbox("Primary Department", departments)
        
        if primary_department != "All Departments":
            # Select secondary departments to coordinate with
            other_departments = [d for d in departments if d != primary_department and d != "All Departments"]
            secondary_departments = st.multiselect("Coordinate With", other_departments)
        else:
            secondary_departments = []
    else:
        from auth import get_user_department
        primary_department = get_user_department()
        st.info(f"Primary Department: {primary_department}")
        
        # Select secondary departments to coordinate with
        departments = ["Public Works", "Health Services", "Education", "Transportation", "Security"]
        other_departments = [d for d in departments if d != primary_department]
        secondary_departments = st.multiselect("Coordinate With", other_departments)
    
    # Coordination type
    coordination_types = ["Resource Sharing", "Joint Projects", "Information Exchange", "All Types"]
    coordination_type = st.selectbox("Coordination Type", coordination_types)

# Main content
if primary_department == "All Departments" and st.session_state.user_role == "administrator":
    # District-wide coordination view
    st.subheader("District-wide Department Coordination")
    
    # Create network visualization placeholder
    st.write("Department Coordination Network")
    
    # Using plotly for network visualization
    departments = ["Public Works", "Health Services", "Education", "Transportation", "Security"]
    
    # Create nodes for departments
    nodes = pd.DataFrame({
        'id': departments,
        'label': departments,
        'size': [30] * len(departments)
    })
    
    # Create edges between departments (connections)
    edges = []
    
    # Generate random coordination connections
    for i, dept1 in enumerate(departments):
        for dept2 in departments[i+1:]:
            # Add random connections
            if np.random.random() > 0.3:  # 70% chance of connection
                weight = np.random.randint(1, 10)
                edges.append({
                    'source': dept1,
                    'target': dept2,
                    'weight': weight
                })
    
    edges_df = pd.DataFrame(edges)
    
    # Create department relationship metrics
    st.subheader("Inter-Department Coordination Metrics")
    
    # Create a matrix of department relationships
    coordination_matrix = pd.DataFrame(0, index=departments, columns=departments)
    
    for _, edge in edges_df.iterrows():
        coordination_matrix.loc[edge['source'], edge['target']] = edge['weight']
        coordination_matrix.loc[edge['target'], edge['source']] = edge['weight']
    
    # Display the coordination matrix
    st.write("Department Coordination Strength (1-10)")
    st.dataframe(coordination_matrix, use_container_width=True)
    
    # Create a heatmap of department coordination
    fig = px.imshow(
        coordination_matrix,
        text_auto=True,
        color_continuous_scale='Blues',
        title="Department Coordination Heatmap"
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Joint projects section
    st.subheader("Cross-Department Projects")
    
    # Create sample cross-department projects
    projects = [
        {
            "project_id": "CDP001",
            "project_name": "City Center Revitalization",
            "departments": ["Public Works", "Transportation", "Security"],
            "status": "In Progress",
            "completion": 45,
            "start_date": "2023-05-15",
            "end_date": "2023-12-30"
        },
        {
            "project_id": "CDP002",
            "project_name": "Public Health Initiative",
            "departments": ["Health Services", "Education"],
            "status": "In Progress",
            "completion": 78,
            "start_date": "2023-03-10",
            "end_date": "2023-11-20"
        },
        {
            "project_id": "CDP003",
            "project_name": "Smart Traffic Management",
            "departments": ["Transportation", "Public Works", "Security"],
            "status": "Planning",
            "completion": 15,
            "start_date": "2023-08-01",
            "end_date": "2024-06-30"
        },
        {
            "project_id": "CDP004",
            "project_name": "Community Safety Program",
            "departments": ["Security", "Health Services", "Education"],
            "status": "Completed",
            "completion": 100,
            "start_date": "2023-01-15",
            "end_date": "2023-07-30"
        }
    ]
    
    # Create a DataFrame for projects
    projects_df = pd.DataFrame(projects)
    
    # Display projects in a more interactive way
    for _, project in projects_df.iterrows():
        with st.expander(f"{project['project_name']} - {project['status']}"):
            st.write(f"**Project ID:** {project['project_id']}")
            st.write(f"**Departments:** {', '.join(project['departments'])}")
            st.write(f"**Timeline:** {project['start_date']} to {project['end_date']}")
            st.progress(project['completion'] / 100)
            st.write(f"**Completion:** {project['completion']}%")
    
    # Resource sharing section
    st.subheader("Resource Sharing Opportunities")
    
    # Create sample resource sharing opportunities
    resources = [
        {
            "resource_id": "RS001",
            "resource_name": "Heavy Equipment Pool",
            "provider": "Public Works",
            "users": ["Transportation", "Security"],
            "status": "Active",
            "utilization": 65
        },
        {
            "resource_id": "RS002",
            "resource_name": "Training Facilities",
            "provider": "Education",
            "users": ["Health Services", "Security"],
            "status": "Active",
            "utilization": 82
        },
        {
            "resource_id": "RS003",
            "resource_name": "Data Analysis Team",
            "provider": "Health Services",
            "users": ["Education", "Transportation"],
            "status": "Proposed",
            "utilization": 0
        },
        {
            "resource_id": "RS004",
            "resource_name": "Community Outreach Network",
            "provider": "Security",
            "users": ["Health Services", "Education", "Public Works"],
            "status": "Active",
            "utilization": 73
        }
    ]
    
    # Create a DataFrame for resources
    resources_df = pd.DataFrame(resources)
    
    # Display resources
    st.dataframe(resources_df, use_container_width=True)
    
    # Add new coordination button
    if st.button("Create New Coordination Initiative"):
        st.info("In a real application, this would open a form to create a new coordination initiative.")
        
else:
    # Department-specific coordination view
    department = primary_department if primary_department != "All Departments" else "Public Works"
    
    st.subheader(f"{department} Coordination Dashboard")
    
    # Current coordination initiatives
    st.write("Current Coordination Initiatives")
    
    # If secondary departments were selected
    if secondary_departments:
        st.success(f"Showing coordination between {department} and {', '.join(secondary_departments)}")
        
        # Create tabs for different coordination types
        coordination_tabs = st.tabs(["Joint Projects", "Resource Sharing", "Information Exchange"])
        
        with coordination_tabs[0]:
            st.write("Joint Projects")
            
            # Sample joint projects
            joint_projects = [
                {
                    "project_id": "JP001",
                    "project_name": f"{department}-{secondary_departments[0]} Infrastructure Project",
                    "departments": [department, secondary_departments[0]],
                    "status": "In Progress",
                    "completion": 60,
                    "start_date": "2023-04-15",
                    "end_date": "2023-12-30"
                }
            ]
            
            # Add more projects if there are more secondary departments
            if len(secondary_departments) > 1:
                joint_projects.append({
                    "project_id": "JP002",
                    "project_name": f"{department}-{secondary_departments[1]} Collaborative Initiative",
                    "departments": [department, secondary_departments[1]],
                    "status": "Planning",
                    "completion": 25,
                    "start_date": "2023-06-01",
                    "end_date": "2024-02-28"
                })
            
            # Display projects
            if joint_projects:
                for project in joint_projects:
                    with st.expander(f"{project['project_name']} - {project['status']}"):
                        st.write(f"**Project ID:** {project['project_id']}")
                        st.write(f"**Departments:** {', '.join(project['departments'])}")
                        st.write(f"**Timeline:** {project['start_date']} to {project['end_date']}")
                        st.progress(project['completion'] / 100)
                        st.write(f"**Completion:** {project['completion']}%")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if st.button("Update Status", key=f"update_{project['project_id']}"):
                                st.success("Status would be updated in a real application")
                        
                        with col2:
                            if st.button("Add Comment", key=f"comment_{project['project_id']}"):
                                st.success("Comment would be added in a real application")
            else:
                st.info("No joint projects found.")
        
        with coordination_tabs[1]:
            st.write("Resource Sharing")
            
            # Shared resources from primary department
            st.write(f"Resources {department} is sharing with other departments:")
            
            shared_resources = [
                {
                    "resource_id": "SR001",
                    "resource_name": f"{department} Specialized Equipment",
                    "shared_with": secondary_departments[0],
                    "status": "Active",
                    "utilization": 70
                }
            ]
            
            if shared_resources:
                for resource in shared_resources:
                    with st.expander(f"{resource['resource_name']} - Shared with {resource['shared_with']}"):
                        st.write(f"**Resource ID:** {resource['resource_id']}")
                        st.write(f"**Status:** {resource['status']}")
                        st.write(f"**Utilization:** {resource['utilization']}%")
                        st.progress(resource['utilization'] / 100)
                        
                        if st.button("Manage Resource", key=f"manage_{resource['resource_id']}"):
                            st.success("Resource management would open in a real application")
            else:
                st.info("No resources being shared.")
            
            # Resources shared with primary department
            st.write(f"Resources shared with {department} from other departments:")
            
            received_resources = [
                {
                    "resource_id": "RR001",
                    "resource_name": f"{secondary_departments[0]} Data Access",
                    "provider": secondary_departments[0],
                    "status": "Active",
                    "utilization": 85
                }
            ]
            
            if received_resources:
                for resource in received_resources:
                    with st.expander(f"{resource['resource_name']} - Provided by {resource['provider']}"):
                        st.write(f"**Resource ID:** {resource['resource_id']}")
                        st.write(f"**Status:** {resource['status']}")
                        st.write(f"**Utilization:** {resource['utilization']}%")
                        st.progress(resource['utilization'] / 100)
                        
                        if st.button("Request Access Change", key=f"request_{resource['resource_id']}"):
                            st.success("Access change request would be sent in a real application")
            else:
                st.info("No resources being received.")
        
        with coordination_tabs[2]:
            st.write("Information Exchange")
            
            # Create sample information exchange items
            info_exchanges = [
                {
                    "exchange_id": "IE001",
                    "exchange_type": "Regular Reports",
                    "departments": [department, secondary_departments[0]],
                    "frequency": "Weekly",
                    "last_exchange": "2023-09-12"
                }
            ]
            
            # Add more if there are more secondary departments
            if len(secondary_departments) > 1:
                info_exchanges.append({
                    "exchange_id": "IE002",
                    "exchange_type": "Data API Access",
                    "departments": [department, secondary_departments[1]],
                    "frequency": "Real-time",
                    "last_exchange": "2023-09-15"
                })
            
            # Display information exchanges
            if info_exchanges:
                for exchange in info_exchanges:
                    with st.expander(f"{exchange['exchange_type']} between {' and '.join(exchange['departments'])}"):
                        st.write(f"**Exchange ID:** {exchange['exchange_id']}")
                        st.write(f"**Frequency:** {exchange['frequency']}")
                        st.write(f"**Last Exchange:** {exchange['last_exchange']}")
                        
                        if st.button("View Exchange History", key=f"history_{exchange['exchange_id']}"):
                            st.success("Exchange history would be displayed in a real application")
            else:
                st.info("No information exchanges found.")
        
        # New coordination initiative section
        st.subheader("Create New Coordination Initiative")
        
        with st.form("new_coordination_form"):
            initiative_type = st.selectbox("Initiative Type", ["Joint Project", "Resource Sharing", "Information Exchange"])
            
            if initiative_type == "Joint Project":
                initiative_name = st.text_input("Project Name")
                initiative_dept = st.multiselect("Departments Involved", [department] + secondary_departments, default=[department])
                start_date = st.date_input("Start Date", datetime.now())
                end_date = st.date_input("End Date", datetime.now() + timedelta(days=90))
                description = st.text_area("Project Description")
            
            elif initiative_type == "Resource Sharing":
                initiative_name = st.text_input("Resource Name")
                provider = st.selectbox("Provider Department", [department] + secondary_departments)
                recipients = st.multiselect("Recipient Departments", [d for d in ([department] + secondary_departments) if d != provider])
                description = st.text_area("Resource Description")
                terms = st.text_area("Terms of Sharing")
            
            else:  # Information Exchange
                initiative_name = st.text_input("Exchange Name")
                initiative_dept = st.multiselect("Departments Involved", [department] + secondary_departments, default=[department])
                frequency = st.selectbox("Exchange Frequency", ["Daily", "Weekly", "Monthly", "Quarterly", "Real-time"])
                data_type = st.text_input("Data Type")
                description = st.text_area("Exchange Description")
            
            submitted = st.form_submit_button("Create Initiative")
            
            if submitted:
                st.success(f"New {initiative_type} coordination initiative would be created in a real application")
                st.info("This is a demo. In a real application, this would create a new coordination initiative.")
    else:
        # No secondary departments selected
        st.info("Please select departments to coordinate with from the sidebar.")
        
        # Show potential coordination opportunities
        st.subheader("Potential Coordination Opportunities")
        
        departments = ["Public Works", "Health Services", "Education", "Transportation", "Security"]
        other_departments = [d for d in departments if d != department]
        
        for other_dept in other_departments:
            with st.expander(f"Potential Coordination with {other_dept}"):
                st.write(f"**Department:** {other_dept}")
                
                # Generate random potential areas
                potential_areas = []
                
                if department == "Public Works" and other_dept == "Transportation":
                    potential_areas = ["Road Infrastructure Projects", "Traffic Management Systems", "Public Facility Maintenance"]
                elif department == "Public Works" and other_dept == "Health Services":
                    potential_areas = ["Healthcare Facility Maintenance", "Water Quality Monitoring", "Waste Management"]
                elif department == "Health Services" and other_dept == "Education":
                    potential_areas = ["School Health Programs", "Health Education Initiatives", "Vaccination Campaigns"]
                else:
                    # Generate generic potential areas
                    area_types = ["Resource Sharing", "Joint Projects", "Information Exchange", "Training Collaboration"]
                    selected_areas = np.random.choice(area_types, size=np.random.randint(1, 4), replace=False)
                    potential_areas = [f"{area} Opportunity" for area in selected_areas]
                
                st.write("**Potential Areas for Coordination:**")
                for area in potential_areas:
                    st.write(f"- {area}")
                
                if st.button(f"Initiate Coordination with {other_dept}"):
                    st.success(f"Coordination with {other_dept} would be initiated in a real application")
                    st.info("Please select the department in the sidebar to continue.")
