import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Function to calculate performance metrics for a department
def calculate_performance_metrics(department):
    """
    Calculates key performance metrics for a specific department.
    
    Parameters:
    - department: Name of the department
    
    Returns:
    - Dictionary containing calculated metrics
    """
    # Department-specific baseline metrics
    if department == "Public Works":
        base_efficiency = 78
        base_budget = 150000
        staff_count = 42
        open_tasks = 18
    elif department == "Health Services":
        base_efficiency = 82
        base_budget = 200000
        staff_count = 65
        open_tasks = 24
    elif department == "Education":
        base_efficiency = 75
        base_budget = 180000
        staff_count = 55
        open_tasks = 21
    elif department == "Transportation":
        base_efficiency = 70
        base_budget = 160000
        staff_count = 38
        open_tasks = 15
    elif department == "Security":
        base_efficiency = 85
        base_budget = 190000
        staff_count = 48
        open_tasks = 19
    else:
        base_efficiency = 75
        base_budget = 150000
        staff_count = 40
        open_tasks = 20
    
    # Random factors for variation
    performance_random = np.random.uniform(0.95, 1.05)
    budget_random = np.random.uniform(0.92, 1.08)
    task_random = np.random.uniform(0.9, 1.1)
    
    # Calculate metrics with randomization
    performance_score = round(base_efficiency * performance_random)
    performance_trend = round((performance_random - 1) * 100)
    
    budget_utilization = round(np.random.uniform(60, 85) * budget_random)
    budget_trend = round((budget_random - 1) * 100)
    
    task_trend = round((task_random - 1) * 100)
    
    # Return calculated metrics
    return {
        'staff_count': staff_count,
        'open_tasks': round(open_tasks * task_random),
        'budget_utilization': budget_utilization,
        'performance_score': performance_score,
        'performance_trend': performance_trend,
        'budget_trend': budget_trend,
        'task_trend': task_trend
    }

# Function to calculate citizen satisfaction metrics
def calculate_satisfaction_metrics(district=None, department=None):
    """
    Calculates citizen satisfaction metrics for a district or department.
    
    Parameters:
    - district: Name of the district (optional)
    - department: Name of the department (optional)
    
    Returns:
    - Dictionary containing satisfaction metrics
    """
    # Base satisfaction score
    base_satisfaction = 82
    
    # Department-specific adjustments
    if department:
        if department == "Public Works":
            dept_factor = 0.97
        elif department == "Health Services":
            dept_factor = 1.05
        elif department == "Education":
            dept_factor = 1.02
        elif department == "Transportation":
            dept_factor = 0.95
        elif department == "Security":
            dept_factor = 1.03
        else:
            dept_factor = 1.0
    else:
        dept_factor = 1.0
    
    # Random variation
    random_factor = np.random.uniform(0.95, 1.05)
    
    # Calculate satisfaction score
    satisfaction_score = round(base_satisfaction * dept_factor * random_factor)
    satisfaction_trend = round((random_factor - 1) * 100)
    
    # Generate time series data for satisfaction trend
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    
    trend_data = []
    current_score = satisfaction_score - (np.random.uniform(5, 15) * satisfaction_trend / abs(satisfaction_trend if satisfaction_trend != 0 else 1))
    
    for month in months:
        # Add some random variation to the trend
        monthly_factor = np.random.uniform(0.98, 1.02)
        current_score = min(100, current_score * monthly_factor)
        
        trend_data.append({
            'month': month,
            'satisfaction_score': round(current_score, 1)
        })
    
    # Return calculated metrics
    return {
        'current_score': satisfaction_score,
        'trend': satisfaction_trend,
        'historical_data': pd.DataFrame(trend_data)
    }

# Function to calculate resource utilization efficiency
def calculate_resource_efficiency(department=None):
    """
    Calculates resource utilization efficiency metrics.
    
    Parameters:
    - department: Name of the department (optional)
    
    Returns:
    - Dictionary containing resource efficiency metrics
    """
    # Base efficiency metrics
    if department:
        if department == "Public Works":
            budget_efficiency = 76
            staff_efficiency = 82
            equipment_efficiency = 73
        elif department == "Health Services":
            budget_efficiency = 84
            staff_efficiency = 89
            equipment_efficiency = 78
        elif department == "Education":
            budget_efficiency = 80
            staff_efficiency = 85
            equipment_efficiency = 72
        elif department == "Transportation":
            budget_efficiency = 71
            staff_efficiency = 79
            equipment_efficiency = 82
        elif department == "Security":
            budget_efficiency = 83
            staff_efficiency = 88
            equipment_efficiency = 86
        else:
            budget_efficiency = 75
            staff_efficiency = 80
            equipment_efficiency = 75
    else:
        # District-wide averages
        budget_efficiency = 78
        staff_efficiency = 84
        equipment_efficiency = 77
    
    # Add random variation
    budget_random = np.random.uniform(0.95, 1.05)
    staff_random = np.random.uniform(0.95, 1.05)
    equipment_random = np.random.uniform(0.95, 1.05)
    
    # Calculate final metrics
    budget_score = round(budget_efficiency * budget_random)
    staff_score = round(staff_efficiency * staff_random)
    equipment_score = round(equipment_efficiency * equipment_random)
    
    # Overall efficiency score (weighted average)
    overall_score = round((budget_score * 0.4) + (staff_score * 0.4) + (equipment_score * 0.2))
    
    # Return calculated metrics
    return {
        'overall_efficiency': overall_score,
        'budget_efficiency': budget_score,
        'staff_efficiency': staff_score,
        'equipment_efficiency': equipment_score,
        'budget_trend': round((budget_random - 1) * 100),
        'staff_trend': round((staff_random - 1) * 100),
        'equipment_trend': round((equipment_random - 1) * 100)
    }

# Function to calculate department comparison metrics
def calculate_department_comparison():
    """
    Calculates comparative metrics across all departments.
    
    Returns:
    - DataFrame containing comparative metrics
    """
    # Department list
    departments = ["Public Works", "Health Services", "Education", "Transportation", "Security"]
    
    # Generate comparison data
    comparison_data = []
    
    for dept in departments:
        # Get base metrics for this department
        metrics = calculate_performance_metrics(dept)
        satisfaction = calculate_satisfaction_metrics(department=dept)
        resource = calculate_resource_efficiency(department=dept)
        
        # Add data point
        comparison_data.append({
            'department': dept,
            'performance_score': metrics['performance_score'],
            'satisfaction_score': satisfaction['current_score'],
            'resource_efficiency': resource['overall_efficiency'],
            'budget_utilization': metrics['budget_utilization'],
            'staff_count': metrics['staff_count'],
            'open_tasks': metrics['open_tasks']
        })
    
    # Return as DataFrame
    return pd.DataFrame(comparison_data)
