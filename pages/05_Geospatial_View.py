import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Geospatial View - District Admin",
    page_icon="🗺️",
    layout="wide"
)

# Authentication check
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to access this page")
    st.stop()

# Page title
st.title("🗺️ Geospatial View")
st.write("View district data on interactive maps")

# Sidebar for filtering
with st.sidebar:
    st.header("Map Options")
    
    # Map view type
    map_views = ["Infrastructure", "Service Requests", "Department Activities", "Public Facilities"]
    selected_view = st.selectbox("Map View", map_views)
    
    # Time period filter
    time_periods = ["Last Week", "Last Month", "Last Quarter", "Year to Date"]
    selected_time = st.selectbox("Time Period", time_periods)
    
    # Department filter (if administrator)
    if st.session_state.user_role == "administrator":
        departments = ["All Departments", "Public Works", "Health Services", "Education", "Transportation", "Security"]
        selected_department = st.selectbox("Department Filter", departments)
    else:
        from auth import get_user_department
        selected_department = get_user_department()
        st.info(f"Viewing data for: {selected_department}")

# Function to generate map data
def generate_map_data(view_type, department=None):
    # Base coordinates (centered around a fictional district)
    # Using New York City coordinates as an example
    base_lat = 40.7128
    base_lng = -74.0060
    
    # Generate points based on view type
    if view_type == "Infrastructure":
        # Generate infrastructure points
        n_points = 20
        points = []
        
        # Types of infrastructure by department
        if department == "Public Works":
            types = ["Road", "Bridge", "Water System", "Sewage System", "Power Line"]
        elif department == "Transportation":
            types = ["Bus Stop", "Traffic Light", "Parking Lot", "Transit Center", "Bike Lane"]
        elif department == "Health Services":
            types = ["Hospital", "Clinic", "Health Center", "Testing Site", "Ambulance Station"]
        elif department == "Education":
            types = ["School", "Library", "Community Center", "Training Center", "Research Facility"]
        elif department == "Security":
            types = ["Police Station", "Fire Station", "Emergency Center", "Security Checkpoint", "Monitoring Station"]
        else:
            types = ["Facility", "Infrastructure", "Service Center", "Public Building", "Equipment"]
        
        for i in range(n_points):
            # Add random variation to base coordinates
            lat = base_lat + np.random.uniform(-0.05, 0.05)
            lng = base_lng + np.random.uniform(-0.05, 0.05)
            
            # Generate random data for this point
            point_type = np.random.choice(types)
            condition = np.random.choice(["Excellent", "Good", "Fair", "Poor", "Critical"])
            last_inspection = (datetime.now() - pd.Timedelta(days=np.random.randint(1, 365))).strftime('%Y-%m-%d')
            
            points.append({
                'id': f"INF{i+1:03d}",
                'lat': lat,
                'lng': lng,
                'type': point_type,
                'name': f"{point_type} {i+1:03d}",
                'condition': condition,
                'last_inspection': last_inspection,
                'department': department if department and department != "All Departments" else np.random.choice(["Public Works", "Transportation", "Health Services", "Education", "Security"])
            })
        
        return pd.DataFrame(points)
    
    elif view_type == "Service Requests":
        # Generate service request points
        n_points = 30
        points = []
        
        # Types of service requests
        request_types = ["Pothole", "Streetlight Out", "Graffiti", "Trash Collection", "Water Leak", 
                        "Noise Complaint", "Traffic Issue", "Building Inspection", "Permit Request"]
        
        # Status options
        statuses = ["Open", "In Progress", "Resolved", "Closed"]
        
        for i in range(n_points):
            # Add random variation to base coordinates
            lat = base_lat + np.random.uniform(-0.05, 0.05)
            lng = base_lng + np.random.uniform(-0.05, 0.05)
            
            # Generate random data for this request
            request_type = np.random.choice(request_types)
            status = np.random.choice(statuses)
            created_date = (datetime.now() - pd.Timedelta(days=np.random.randint(1, 30))).strftime('%Y-%m-%d')
            
            # Assign to a department based on request type
            if request_type in ["Pothole", "Streetlight Out", "Water Leak"]:
                assigned_dept = "Public Works"
            elif request_type in ["Traffic Issue"]:
                assigned_dept = "Transportation"
            elif request_type in ["Building Inspection", "Permit Request"]:
                assigned_dept = "Education"
            elif request_type in ["Noise Complaint", "Graffiti"]:
                assigned_dept = "Security"
            else:
                assigned_dept = np.random.choice(["Public Works", "Health Services", "Education", "Transportation", "Security"])
            
            # Filter by department if specified
            if department and department != "All Departments" and assigned_dept != department:
                continue
            
            points.append({
                'id': f"SR{i+1:03d}",
                'lat': lat,
                'lng': lng,
                'type': request_type,
                'status': status,
                'created_date': created_date,
                'department': assigned_dept
            })
        
        return pd.DataFrame(points)
    
    elif view_type == "Department Activities":
        # Generate department activity points
        n_points = 15
        points = []
        
        # Types of activities by department
        activity_types = {
            "Public Works": ["Construction", "Maintenance", "Inspection", "Installation", "Repair"],
            "Health Services": ["Vaccination", "Inspection", "Community Outreach", "Health Screening", "Training"],
            "Education": ["School Event", "Training Program", "Community Workshop", "Facility Improvement", "Research"],
            "Transportation": ["Traffic Study", "Road Work", "Transit Improvement", "Infrastructure Project", "Planning"],
            "Security": ["Patrol", "Community Meeting", "Training Exercise", "Emergency Response", "Safety Inspection"]
        }
        
        # If department is specified, only show activities for that department
        if department and department != "All Departments":
            departments_to_show = [department]
        else:
            departments_to_show = list(activity_types.keys())
        
        for dept in departments_to_show:
            for i in range(n_points // len(departments_to_show)):
                # Add random variation to base coordinates
                lat = base_lat + np.random.uniform(-0.05, 0.05)
                lng = base_lng + np.random.uniform(-0.05, 0.05)
                
                # Generate random data for this activity
                activity = np.random.choice(activity_types[dept])
                status = np.random.choice(["Planned", "In Progress", "Completed"])
                start_date = (datetime.now() - pd.Timedelta(days=np.random.randint(1, 30))).strftime('%Y-%m-%d')
                
                points.append({
                    'id': f"{dept[:3].upper()}{i+1:03d}",
                    'lat': lat,
                    'lng': lng,
                    'type': activity,
                    'status': status,
                    'start_date': start_date,
                    'department': dept
                })
        
        return pd.DataFrame(points)
    
    elif view_type == "Public Facilities":
        # Generate public facility points
        n_points = 25
        points = []
        
        # Types of facilities
        facility_types = ["School", "Library", "Community Center", "Park", "Hospital", "Clinic", 
                         "Police Station", "Fire Station", "Government Office", "Recreation Center"]
        
        for i in range(n_points):
            # Add random variation to base coordinates
            lat = base_lat + np.random.uniform(-0.05, 0.05)
            lng = base_lng + np.random.uniform(-0.05, 0.05)
            
            # Generate random data for this facility
            facility_type = np.random.choice(facility_types)
            
            # Assign to a department based on facility type
            if facility_type in ["School", "Library", "Community Center"]:
                assigned_dept = "Education"
            elif facility_type in ["Hospital", "Clinic"]:
                assigned_dept = "Health Services"
            elif facility_type in ["Police Station", "Fire Station"]:
                assigned_dept = "Security"
            elif facility_type in ["Park", "Recreation Center"]:
                assigned_dept = "Public Works"
            else:
                assigned_dept = np.random.choice(["Public Works", "Health Services", "Education", "Transportation", "Security"])
            
            # Filter by department if specified
            if department and department != "All Departments" and assigned_dept != department:
                continue
            
            points.append({
                'id': f"FAC{i+1:03d}",
                'lat': lat,
                'lng': lng,
                'type': facility_type,
                'name': f"{facility_type} {i+1:03d}",
                'status': np.random.choice(["Operational", "Limited Service", "Closed for Maintenance", "Under Construction"]),
                'department': assigned_dept
            })
        
        return pd.DataFrame(points)
    
    else:
        # Return empty dataframe if view type not recognized
        return pd.DataFrame()

# Main content
selected_department_filter = selected_department if st.session_state.user_role == "administrator" else selected_department

# Generate map data based on selection
map_data = generate_map_data(selected_view, department=selected_department_filter)

# Check if we have data to display
if not map_data.empty:
    # Create a container for the map and info
    st.subheader(f"{selected_view} Map")
    
    # Map visualization options
    map_container = st.container()
    
    with map_container:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Create map using Plotly
            if 'type' in map_data.columns:
                # Color by type
                fig = px.scatter_mapbox(
                    map_data, 
                    lat="lat", 
                    lon="lng", 
                    hover_name="id",
                    color="type",
                    zoom=10,
                    mapbox_style="carto-positron"
                )
            elif 'status' in map_data.columns:
                # Color by status
                fig = px.scatter_mapbox(
                    map_data, 
                    lat="lat", 
                    lon="lng", 
                    hover_name="id",
                    color="status",
                    zoom=10,
                    mapbox_style="carto-positron"
                )
            else:
                # Basic map
                fig = px.scatter_mapbox(
                    map_data, 
                    lat="lat", 
                    lon="lng", 
                    hover_name="id",
                    zoom=10,
                    mapbox_style="carto-positron"
                )
            
            fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("Map Filters")
            
            # Add appropriate filters based on the view type
            if selected_view == "Infrastructure":
                # Filter by infrastructure type
                if 'type' in map_data.columns:
                    types = ['All'] + sorted(map_data['type'].unique().tolist())
                    selected_type = st.selectbox("Infrastructure Type", types)
                    
                    if selected_type != 'All':
                        map_data = map_data[map_data['type'] == selected_type]
                
                # Filter by condition
                if 'condition' in map_data.columns:
                    conditions = ['All'] + sorted(map_data['condition'].unique().tolist())
                    selected_condition = st.selectbox("Condition", conditions)
                    
                    if selected_condition != 'All':
                        map_data = map_data[map_data['condition'] == selected_condition]
            
            elif selected_view == "Service Requests":
                # Filter by request type
                if 'type' in map_data.columns:
                    types = ['All'] + sorted(map_data['type'].unique().tolist())
                    selected_type = st.selectbox("Request Type", types)
                    
                    if selected_type != 'All':
                        map_data = map_data[map_data['type'] == selected_type]
                
                # Filter by status
                if 'status' in map_data.columns:
                    statuses = ['All'] + sorted(map_data['status'].unique().tolist())
                    selected_status = st.selectbox("Status", statuses)
                    
                    if selected_status != 'All':
                        map_data = map_data[map_data['status'] == selected_status]
            
            elif selected_view == "Department Activities":
                # Filter by activity type
                if 'type' in map_data.columns:
                    types = ['All'] + sorted(map_data['type'].unique().tolist())
                    selected_type = st.selectbox("Activity Type", types)
                    
                    if selected_type != 'All':
                        map_data = map_data[map_data['type'] == selected_type]
                
                # Filter by status
                if 'status' in map_data.columns:
                    statuses = ['All'] + sorted(map_data['status'].unique().tolist())
                    selected_status = st.selectbox("Status", statuses)
                    
                    if selected_status != 'All':
                        map_data = map_data[map_data['status'] == selected_status]
            
            elif selected_view == "Public Facilities":
                # Filter by facility type
                if 'type' in map_data.columns:
                    types = ['All'] + sorted(map_data['type'].unique().tolist())
                    selected_type = st.selectbox("Facility Type", types)
                    
                    if selected_type != 'All':
                        map_data = map_data[map_data['type'] == selected_type]
                
                # Filter by status
                if 'status' in map_data.columns:
                    statuses = ['All'] + sorted(map_data['status'].unique().tolist())
                    selected_status = st.selectbox("Status", statuses)
                    
                    if selected_status != 'All':
                        map_data = map_data[map_data['status'] == selected_status]
            
            # Show summary stats for the filtered data
            st.write("### Summary")
            st.write(f"Total Points: {len(map_data)}")
            
            if 'department' in map_data.columns:
                dept_counts = map_data['department'].value_counts()
                st.write("By Department:")
                for dept, count in dept_counts.items():
                    st.write(f"- {dept}: {count}")
            
            if 'type' in map_data.columns:
                type_counts = map_data['type'].value_counts()
                st.write("By Type:")
                for type_name, count in type_counts.head(5).items():
                    st.write(f"- {type_name}: {count}")
                
                if len(type_counts) > 5:
                    st.write(f"- Others: {type_counts[5:].sum()}")
            
            if 'status' in map_data.columns:
                status_counts = map_data['status'].value_counts()
                st.write("By Status:")
                for status, count in status_counts.items():
                    st.write(f"- {status}: {count}")
    
    # Show data table below the map
    with st.expander("View Data Table"):
        st.dataframe(map_data, use_container_width=True)
    
    # Additional actions based on view type
    if selected_view == "Infrastructure":
        st.subheader("Infrastructure Management")
        
        if st.button("Schedule Inspections for Selected Areas"):
            st.success("Inspection scheduling would be initiated in a real application")
            st.info("This is a demo. In a real application, this would schedule inspections.")
        
        if st.button("Generate Infrastructure Report"):
            st.success("Infrastructure report would be generated in a real application")
            st.info("This is a demo. In a real application, this would generate a detailed report.")
    
    elif selected_view == "Service Requests":
        st.subheader("Service Request Management")
        
        if st.button("Assign Resources to Open Requests"):
            st.success("Resource assignment would be initiated in a real application")
            st.info("This is a demo. In a real application, this would assign resources to open requests.")
        
        if st.button("Generate Service Request Report"):
            st.success("Service request report would be generated in a real application")
            st.info("This is a demo. In a real application, this would generate a detailed report.")
    
    elif selected_view == "Department Activities":
        st.subheader("Activity Management")
        
        if st.button("Coordinate Activities in Selected Area"):
            st.success("Activity coordination would be initiated in a real application")
            st.info("This is a demo. In a real application, this would help coordinate activities.")
        
        if st.button("Generate Activity Report"):
            st.success("Activity report would be generated in a real application")
            st.info("This is a demo. In a real application, this would generate a detailed report.")
    
    elif selected_view == "Public Facilities":
        st.subheader("Facility Management")
        
        if st.button("Schedule Maintenance for Selected Facilities"):
            st.success("Maintenance scheduling would be initiated in a real application")
            st.info("This is a demo. In a real application, this would schedule maintenance.")
        
        if st.button("Generate Facility Report"):
            st.success("Facility report would be generated in a real application")
            st.info("This is a demo. In a real application, this would generate a detailed report.")
else:
    st.error("No data available for the selected view and filters.")
