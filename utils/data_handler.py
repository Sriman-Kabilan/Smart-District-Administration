import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Function to generate department data
def get_department_data(department=None):
    # Department list
    departments = ["Public Works", "Health Services", "Education", "Transportation", "Security"]
    
    # If no department specified, return data for all departments
    if department is None:
        data = []
        for dept in departments:
            dept_data = _generate_department_data(dept)
            data.extend(dept_data)
        return pd.DataFrame(data)
    else:
        # Return data for specific department
        dept_data = _generate_department_data(department)
        return pd.DataFrame(dept_data)

# Helper function to generate consistent department data
def _generate_department_data(department):
    # Generate data for last 12 weeks
    weeks = pd.date_range(end=datetime.now(), periods=12, freq='W').tolist()
    
    # Department-specific baseline metrics
    if department == "Public Works":
        base_efficiency = 78
        base_budget = 150000
        task_factor = 1.2
    elif department == "Health Services":
        base_efficiency = 82
        base_budget = 200000
        task_factor = 1.5
    elif department == "Education":
        base_efficiency = 75
        base_budget = 180000
        task_factor = 1.0
    elif department == "Transportation":
        base_efficiency = 70
        base_budget = 160000
        task_factor = 0.9
    elif department == "Security":
        base_efficiency = 85
        base_budget = 190000
        task_factor = 1.3
    else:
        base_efficiency = 75
        base_budget = 150000
        task_factor = 1.0
    
    data = []
    for i, week in enumerate(weeks):
        # Create some variation over time
        week_factor = 1 + (i * 0.02)  # Slight improvement over time
        random_factor = np.random.uniform(0.9, 1.1)  # Random variation
        
        efficiency = min(100, base_efficiency * week_factor * random_factor)
        budget_spent = (base_budget / 12) * week_factor * random_factor
        tasks_total = round(25 * task_factor * week_factor)
        tasks_completed = round(tasks_total * (efficiency / 100))
        
        data.append({
            'department': department,
            'week': week.strftime('%Y-%m-%d'),
            'efficiency_score': round(efficiency, 1),
            'budget_spent': round(budget_spent, 2),
            'tasks_total': tasks_total,
            'tasks_completed': tasks_completed,
            'resource_utilization': round(min(100, efficiency * random_factor), 1)
        })
    
    return data

# Function to get performance data
def get_performance_data(department=None, all_departments=False, by_staff=False):
    if all_departments:
        # Generate data for all departments
        departments = ["Public Works", "Health Services", "Education", "Transportation", "Security"]
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        
        data = []
        for dept in departments:
            dept_efficiency = np.random.uniform(65, 95)
            
            # Single row for bar chart
            data.append({
                'department': dept,
                'efficiency_score': round(dept_efficiency, 1),
                'budget_utilization': round(np.random.uniform(60, 95), 1)
            })
            
            # Monthly data for line chart
            for month in months:
                random_factor = np.random.uniform(0.9, 1.1)
                data.append({
                    'department': dept,
                    'month': month,
                    'task_completion_rate': round(min(100, dept_efficiency * random_factor), 1)
                })
        
        return pd.DataFrame(data)
    
    elif by_staff and department:
        # Generate staff performance data for the specified department
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
        
        data = []
        for staff_name in staff_list:
            base_efficiency = np.random.uniform(60, 95)
            tasks_completed = int(np.random.uniform(15, 40))
            
            data.append({
                'department': department,
                'staff_name': staff_name,
                'efficiency_score': round(base_efficiency, 1),
                'tasks_completed': tasks_completed,
                'tasks_in_progress': int(np.random.uniform(2, 10))
            })
        
        return pd.DataFrame(data)
    
    elif department:
        # Generate performance data for specific department
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        
        # Get base efficiency for the department
        if department == "Public Works":
            base_efficiency = 78
        elif department == "Health Services":
            base_efficiency = 82
        elif department == "Education":
            base_efficiency = 75
        elif department == "Transportation":
            base_efficiency = 70
        elif department == "Security":
            base_efficiency = 85
        else:
            base_efficiency = 75
        
        data = []
        for i, month in enumerate(months):
            # Create some variation over time
            month_factor = 1 + (i * 0.03)  # Improvement over time
            random_factor = np.random.uniform(0.9, 1.1)  # Random variation
            
            efficiency = min(100, base_efficiency * month_factor * random_factor)
            
            data.append({
                'department': department,
                'month': month,
                'efficiency_score': round(efficiency, 1),
                'task_completion_rate': round(min(100, efficiency * random_factor), 1)
            })
        
        return pd.DataFrame(data)
    
    else:
        # Return empty dataframe if no valid options provided
        return pd.DataFrame()

# Function to get resource data
def get_resource_data(department=None, all_departments=False):
    # Department budgets
    department_budgets = {
        "Public Works": 1500000,
        "Health Services": 2000000,
        "Education": 1800000,
        "Transportation": 1600000,
        "Security": 1900000
    }
    
    if all_departments:
        # Return budget allocation for all departments
        data = []
        for dept, budget in department_budgets.items():
            data.append({
                'department': dept,
                'budget_allocation': budget,
                'budget_spent': round(budget * np.random.uniform(0.6, 0.9), 2)
            })
        
        return pd.DataFrame(data)
    
    elif department and department in department_budgets:
        # Return detailed resource data for specific department
        budget = department_budgets[department]
        
        # Resource categories
        categories = ["Personnel", "Equipment", "Operations", "Maintenance", "Development"]
        
        # Allocate budget percentages to categories
        category_percentages = np.random.dirichlet(np.ones(len(categories)), size=1)[0]
        
        data = []
        for i, category in enumerate(categories):
            allocation = budget * category_percentages[i]
            spent = allocation * np.random.uniform(0.5, 0.95)
            
            data.append({
                'department': department,
                'category': category,
                'allocation': round(allocation, 2),
                'spent': round(spent, 2),
                'remaining': round(allocation - spent, 2)
            })
        
        return pd.DataFrame(data)
    
    else:
        # Return empty dataframe if no valid options provided
        return pd.DataFrame()

# Function to get task data
def get_task_data(department=None, staff=None):
    # Task statuses
    statuses = ["Pending", "In Progress", "Completed"]
    
    # Task priorities
    priorities = ["Low", "Medium", "High", "Critical"]
    
    # Generate task data based on parameters
    if department:
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
        
        # Task types by department
        if department == "Public Works":
            task_types = ["Road Maintenance", "Building Inspection", "Water System Repair", "Parks Maintenance"]
        elif department == "Health Services":
            task_types = ["Vaccination Drive", "Health Inspection", "Medical Supply Inventory", "Health Education"]
        elif department == "Education":
            task_types = ["Curriculum Review", "Teacher Training", "School Inspection", "Student Services"]
        elif department == "Transportation":
            task_types = ["Traffic Analysis", "Route Planning", "Vehicle Maintenance", "Transit Inspection"]
        elif department == "Security":
            task_types = ["Security Assessment", "Staff Training", "Equipment Maintenance", "Patrol Scheduling"]
        else:
            task_types = ["Type 1", "Type 2", "Type 3", "Type 4"]
        
        # Filter by staff if specified
        if staff:
            staff_list = [s for s in staff_list if s == staff]
        
        # Generate tasks
        data = []
        task_id_counter = 1001
        
        # Number of tasks to generate
        num_tasks = 5 if staff else 20
        
        for _ in range(num_tasks):
            assigned_to = np.random.choice(staff_list)
            task_type = np.random.choice(task_types)
            status = np.random.choice(statuses)
            priority = np.random.choice(priorities)
            
            # Generate random dates
            start_date = datetime.now() - timedelta(days=np.random.randint(1, 30))
            due_date = start_date + timedelta(days=np.random.randint(3, 21))
            
            data.append({
                'task_id': f"T{task_id_counter}",
                'task_name': f"{task_type} - {task_id_counter}",
                'description': f"Complete {task_type.lower()} activities as assigned.",
                'department': department,
                'assigned_to': assigned_to,
                'status': status,
                'priority': priority,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'due_date': due_date.strftime('%Y-%m-%d')
            })
            
            task_id_counter += 1
        
        return pd.DataFrame(data)
    
    else:
        # Return empty dataframe if no department specified
        return pd.DataFrame()
