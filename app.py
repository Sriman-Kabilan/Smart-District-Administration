import streamlit as st
from auth import authenticate_user, create_user_data, check_user_auth, register_user
from dashboard import display_admin_dashboard, display_department_head_dashboard, display_staff_dashboard
import os

# Configure page settings
st.set_page_config(
    page_title="Smart District Administration Dashboard",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "username" not in st.session_state:
    st.session_state.username = None
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"

# Create initial user data if not already done
if "user_data_created" not in st.session_state:
    create_user_data()
    st.session_state.user_data_created = True

# Main app container
def main():
    # Sidebar for authentication
    with st.sidebar:
        st.title("🏙️ District Admin")
        
        if not st.session_state.authenticated:
            st.subheader("Login")
            login_tab, register_tab = st.tabs(["Login", "Register"])
            
            with login_tab:
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")
                
                # Display sample user credentials
                with st.expander("Available Test Users"):
                    st.markdown("""
                    ### Administrator
                    - Username: `admin`
                    - Password: `admin123`
                    
                    ### Department Heads
                    - Public Works: `public_works_head` (Password: `dept123`)
                    - Health Services: `health_head` (Password: `dept123`)
                    - Education: `education_head` (Password: `dept123`)
                    - Transportation: `transportation_head` (Password: `dept123`)
                    - Security: `security_head` (Password: `dept123`)
                    
                    ### Staff Members
                    - Public Works: `pw_staff1`, `pw_staff2`, `pw_staff3` (Password: `staff123`)
                    - Health Services: `health_staff1`, `health_staff2` (Password: `staff123`)
                    - Other Departments: Various staff usernames with `staff123` password
                    """)
                
                if st.button("Login", key="login_button"):
                    authentication_status, user_role = authenticate_user(username, password)
                    
                    if authentication_status:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.user_role = user_role
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
            
            with register_tab:
                with st.form("registration_form"):
                    st.subheader("Register New Account")
                    
                    # Personal information
                    full_name = st.text_input("Full Name", key="reg_full_name")
                    username = st.text_input("Username", key="reg_username")
                    email = st.text_input("Email", key="reg_email")
                    
                    # Password fields
                    password = st.text_input("Password", type="password", key="reg_password")
                    confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
                    
                    # Role and department
                    role = st.selectbox(
                        "Role", 
                        ["staff", "department_head"],
                        index=0,
                        key="reg_role"
                    )
                    
                    department = st.selectbox(
                        "Department",
                        ["Public Works", "Health Services", "Education", "Transportation", "Security"],
                        key="reg_department"
                    )
                    
                    # Admin code for special roles
                    admin_code = ""
                    if role == "department_head":
                        admin_code = st.text_input("Administrator Code", type="password", key="reg_admin_code")
                    
                    # Submit button
                    submit_button = st.form_submit_button("Register")
                    
                    if submit_button:
                        # Validate inputs
                        if not full_name or not username or not email or not password:
                            st.error("Please fill in all required fields")
                        elif password != confirm_password:
                            st.error("Passwords do not match")
                        elif role == "department_head" and admin_code != "admin2025":  # Simple admin code for demo
                            st.error("Invalid administrator code for department head registration")
                        else:
                            # Register the user
                            success, message, user_id = register_user(
                                username=username,
                                password=password,
                                full_name=full_name,
                                email=email,
                                role=role,
                                department=department
                            )
                            
                            if success:
                                st.success(f"Registration successful! You can now log in as {username}")
                            else:
                                st.error(f"Registration failed: {message}")
                
                st.info("Administrator accounts can only be created by existing administrators through the admin panel.")
        else:
            st.success(f"Logged in as: {st.session_state.username}")
            st.write(f"Role: {st.session_state.user_role}")
            
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.session_state.username = None
                st.session_state.user_role = None
                st.rerun()
    
    # Main content area
    if not st.session_state.authenticated:
        st.title("Smart District Administration Dashboard")
        st.markdown("""
        Welcome to the Smart District Administration Dashboard. Please login to access the system.
        
        This platform provides:
        - Real-time data visualization
        - Performance monitoring
        - Resource management
        - Task tracking
        - Department coordination
        - Geospatial data integration
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("📊 Real-time Analytics")
        with col2:
            st.info("🗺️ Geospatial Integration")
        with col3:
            st.info("📋 Performance Monitoring")
            
    else:
        # Display role-based dashboard
        if st.session_state.user_role == "administrator":
            display_admin_dashboard()
        elif st.session_state.user_role == "department_head":
            display_department_head_dashboard()
        elif st.session_state.user_role == "staff":
            display_staff_dashboard()
        else:
            st.error("Unknown user role. Please contact the administrator.")

# Run the main function
if __name__ == "__main__":
    main()
