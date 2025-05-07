import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

# Function to create a KPI card with uniform styling
def create_kpi_card(title, value, delta=None, color="#1E88E5"):
    """
    Creates a styled KPI card with a title, value, and optional delta indicator.
    
    Parameters:
    - title: Title of the KPI card
    - value: Main value to display
    - delta: Change indicator (optional)
    - color: Accent color for the card
    """
    st.markdown(
        f"""
        <div style="padding: 10px; border-radius: 5px; border-left: 5px solid {color}; background-color: #f8f9fa;">
            <h3 style="color: #424242; margin: 0; font-size: 1.1rem;">{title}</h3>
            <div style="display: flex; align-items: baseline;">
                <span style="color: {color}; font-size: 1.8rem; font-weight: bold; margin-right: 10px;">{value}</span>
                <span style="color: #757575; font-size: 0.9rem;">{delta if delta else ''}</span>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Function to create a performance chart
def create_performance_chart(data, time_period='weekly'):
    """
    Creates an interactive performance chart using Altair.
    
    Parameters:
    - data: DataFrame containing performance data
    - time_period: Time period for the chart ('weekly', 'monthly', etc.)
    
    Returns:
    - Altair chart object
    """
    # Ensure data is a DataFrame
    if not isinstance(data, pd.DataFrame):
        return None
    
    # Check if data has required columns
    required_cols = ['efficiency_score', 'tasks_completed']
    time_col = 'week' if time_period == 'weekly' else 'month'
    
    if not all(col in data.columns for col in required_cols + [time_col]):
        return None
    
    # Create base chart
    base = alt.Chart(data).encode(
        x=alt.X(f'{time_col}:O', title=time_period.capitalize())
    )
    
    # Create line chart for efficiency score
    line = base.mark_line(strokeWidth=3, color='#1E88E5').encode(
        y=alt.Y('efficiency_score:Q', title='Efficiency Score', scale=alt.Scale(domain=[0, 100])),
        tooltip=[time_col, 'efficiency_score', 'tasks_completed']
    )
    
    # Create bar chart for tasks completed
    bar = base.mark_bar(color='#43A047').encode(
        y=alt.Y('tasks_completed:Q', title='Tasks Completed'),
        tooltip=[time_col, 'tasks_completed']
    )
    
    # Combine charts with dual axis
    chart = alt.layer(line, bar).resolve_scale(
        y='independent'
    ).properties(
        title=f'Performance Metrics ({time_period.capitalize()})',
        width='container',
        height=300
    ).interactive()
    
    return chart

# Function to create a resource allocation chart
def create_resource_chart(data):
    """
    Creates a resource allocation chart using Altair.
    
    Parameters:
    - data: DataFrame containing resource data
    
    Returns:
    - Altair chart object
    """
    # Ensure data has budget data
    if 'budget_spent' not in data.columns:
        # Try to get resource data
        import utils.data_handler as dh
        department = data['department'].iloc[0] if 'department' in data.columns else None
        if department:
            resource_data = dh.get_resource_data(department=department)
        else:
            return None
    else:
        # Use aggregated data from provided DataFrame
        budget_data = data.groupby('week')['budget_spent'].sum().reset_index()
        budget_data['category'] = 'Total'
        resource_data = budget_data
    
    # Create chart
    chart = alt.Chart(resource_data).mark_bar().encode(
        x=alt.X('category:N', title='Resource Category'),
        y=alt.Y('spent:Q', title='Amount Spent'),
        color=alt.Color('category:N', scale=alt.Scale(scheme='blues')),
        tooltip=['category', 'spent', 'allocation']
    ).properties(
        title='Resource Allocation and Utilization',
        width='container',
        height=300
    ).interactive()
    
    return chart

# Function to create a geospatial heatmap
def create_heatmap(data, location_field, value_field, center=[40.7128, -74.0060]):
    """
    Creates a heatmap visualization for geospatial data.
    
    Parameters:
    - data: DataFrame containing geospatial data
    - location_field: Field containing location information
    - value_field: Field containing values for the heatmap
    - center: Center coordinates for the map [lat, lng]
    
    Returns:
    - Folium map object
    """
    try:
        import folium
        from folium.plugins import HeatMap
        from streamlit_folium import folium_static
        
        # Create base map
        m = folium.Map(location=center, zoom_start=12)
        
        # Add heatmap layer
        heat_data = [[row['lat'], row['lng'], row[value_field]] for _, row in data.iterrows()]
        HeatMap(heat_data).add_to(m)
        
        return m
    except ImportError:
        st.error("Required packages not available. Please install folium and streamlit-folium.")
        return None

# Function to create an interactive data table
def create_interactive_table(data, editable_columns=None):
    """
    Creates an interactive data table with optional editing capabilities.
    
    Parameters:
    - data: DataFrame containing table data
    - editable_columns: List of column names that should be editable
    
    Returns:
    - Streamlit AgGrid object
    """
    try:
        from st_aggrid import AgGrid, GridOptionsBuilder
        
        # Configure grid options
        gb = GridOptionsBuilder.from_dataframe(data)
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
        gb.configure_selection('single')
        
        if editable_columns:
            for col in editable_columns:
                if col in data.columns:
                    gb.configure_column(col, editable=True)
        
        grid_options = gb.build()
        
        # Create and return the grid
        return AgGrid(data, gridOptions=grid_options, update_mode='MODEL_CHANGED', fit_columns_on_grid_load=True)
    except ImportError:
        # Fallback to standard dataframe if AgGrid is not available
        st.dataframe(data)
        return data
