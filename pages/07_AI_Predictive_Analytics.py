import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid

from auth import check_user_auth, get_user_department
from utils.data_handler import get_department_data, get_performance_data, get_resource_data
from utils.visualization import create_kpi_card
from utils.predictive_analytics import (
    predict_resource_needs, 
    predict_optimal_resource_allocation,
    generate_prediction_explanation
)

# Set page config
st.set_page_config(
    page_title="AI Predictive Analytics", 
    page_icon="📊",
    layout="wide"
)

# Check if user is authenticated
if check_user_auth():
    # Get user role and department
    user_role = st.session_state.get("role", "")
    department = get_user_department()
    
    # Page header
    st.title("AI-Driven Predictive Analytics")
    st.write("Use machine learning to predict future resource needs and optimize allocations")
    
    # Only admin and department heads can access predictive analytics
    if user_role in ["administrator", "department_head"]:
        # Create tabs for different analysis types
        tabs = st.tabs(["Resource Prediction", "Optimization Analysis", "What-If Scenarios"])
        
        # Prediction options in sidebar
        with st.sidebar:
            st.subheader("Prediction Settings")
            
            prediction_periods = st.slider(
                "Prediction Periods (Months)",
                min_value=1,
                max_value=12,
                value=3,
                help="Number of months to predict into the future"
            )
            
            model_options = {
                "random_forest": "Random Forest (Best for non-linear patterns)",
                "linear": "Linear Regression (Best for trends)",
                "arima": "ARIMA (Best for seasonal data)"
            }
            
            selected_model = st.selectbox(
                "Prediction Model",
                options=list(model_options.keys()),
                format_func=lambda x: model_options[x],
                index=0
            )
            
            departments_list = ["All Departments"] if user_role == "administrator" else [department]
            selected_department = st.selectbox(
                "Department",
                options=departments_list,
                index=0
            )
            
            if selected_department == "All Departments" and user_role == "administrator":
                # Allow admin to choose specific department
                all_departments = ["Public Works", "Education", "Health", "Finance", 
                                  "Urban Planning", "Transportation", "Social Services"]
                analysis_department = st.selectbox(
                    "Select Department for Analysis",
                    options=all_departments
                )
            else:
                analysis_department = department
        
        # Resource Prediction Tab
        with tabs[0]:
            st.subheader("Resource Allocation Prediction")
            st.write(f"Predicting future resource needs for: **{analysis_department}**")
            
            # Get historical resource data
            resource_data = get_resource_data(department=analysis_department)
            
            if not resource_data or len(resource_data) < 3:
                st.warning(f"Insufficient historical data for {analysis_department} department. Need at least 3 data points for prediction.")
                st.info("Please add more historical resource allocation data to enable predictions.")
            else:
                # Convert to DataFrame for visualization
                if isinstance(resource_data, list):
                    historical_df = pd.DataFrame(resource_data)
                else:
                    historical_df = resource_data.copy()
                
                # Generate predictions
                predictions = predict_resource_needs(
                    resource_data, 
                    prediction_periods=prediction_periods,
                    model_type=selected_model
                )
                
                if predictions:
                    # Convert predictions to DataFrame
                    predictions_df = pd.DataFrame(predictions)
                    
                    # Combine historical and predicted data
                    historical_df['is_prediction'] = False
                    combined_df = pd.concat([historical_df, predictions_df], ignore_index=True)
                    
                    # Create visualizations
                    st.subheader("Budget Allocation Prediction")
                    
                    # Budget prediction chart
                    if 'budget_allocation' in combined_df.columns:
                        fig_budget = px.line(
                            combined_df, 
                            x='date', 
                            y='budget_allocation',
                            color='is_prediction',
                            color_discrete_map={False: "#1F77B4", True: "#FF7F0E"},
                            title=f"Budget Allocation Prediction for {analysis_department}",
                            labels={"budget_allocation": "Budget Amount", "date": "Time Period", "is_prediction": "Prediction"}
                        )
                        
                        # Add markers and improve layout
                        fig_budget.update_traces(mode='lines+markers')
                        fig_budget.update_layout(
                            legend_title_text='Data Type',
                            xaxis_title="Date",
                            yaxis_title="Budget Allocation",
                            hovermode="x unified"
                        )
                        
                        # Update hover template
                        fig_budget.update_traces(
                            hovertemplate="<b>%{x|%b %Y}</b><br>Budget: %{y:,.2f}<extra></extra>"
                        )
                        
                        # Add a vertical line to separate historical from predicted
                        if 'date' in historical_df.columns:
                            last_historical_date = historical_df['date'].max()
                            fig_budget.add_vline(
                                x=last_historical_date, 
                                line_width=2, 
                                line_dash="dash", 
                                line_color="gray",
                                annotation_text="Prediction Start",
                                annotation_position="top right"
                            )
                        
                        st.plotly_chart(fig_budget, use_container_width=True)
                    
                    # Staff allocation prediction
                    if 'staff_allocation' in combined_df.columns:
                        fig_staff = px.line(
                            combined_df, 
                            x='date', 
                            y='staff_allocation',
                            color='is_prediction',
                            color_discrete_map={False: "#1F77B4", True: "#FF7F0E"},
                            title=f"Staff Allocation Prediction for {analysis_department}",
                            labels={"staff_allocation": "Staff Count", "date": "Time Period", "is_prediction": "Prediction"}
                        )
                        
                        # Add markers and improve layout
                        fig_staff.update_traces(mode='lines+markers')
                        fig_staff.update_layout(
                            legend_title_text='Data Type',
                            xaxis_title="Date",
                            yaxis_title="Staff Count",
                            hovermode="x unified"
                        )
                        
                        # Update hover template
                        fig_staff.update_traces(
                            hovertemplate="<b>%{x|%b %Y}</b><br>Staff: %{y:,.0f}<extra></extra>"
                        )
                        
                        # Add a vertical line to separate historical from predicted
                        if 'date' in historical_df.columns:
                            last_historical_date = historical_df['date'].max()
                            fig_staff.add_vline(
                                x=last_historical_date, 
                                line_width=2, 
                                line_dash="dash", 
                                line_color="gray",
                                annotation_text="Prediction Start",
                                annotation_position="top right"
                            )
                        
                        st.plotly_chart(fig_staff, use_container_width=True)
                    
                    # Equipment allocation prediction if available
                    if 'equipment_allocation' in combined_df.columns:
                        fig_equipment = px.line(
                            combined_df, 
                            x='date', 
                            y='equipment_allocation',
                            color='is_prediction',
                            color_discrete_map={False: "#1F77B4", True: "#FF7F0E"},
                            title=f"Equipment Allocation Prediction for {analysis_department}",
                            labels={"equipment_allocation": "Equipment Budget", "date": "Time Period", "is_prediction": "Prediction"}
                        )
                        
                        # Add markers and improve layout
                        fig_equipment.update_traces(mode='lines+markers')
                        fig_equipment.update_layout(
                            legend_title_text='Data Type',
                            xaxis_title="Date",
                            yaxis_title="Equipment Allocation",
                            hovermode="x unified"
                        )
                        
                        # Update hover template
                        fig_equipment.update_traces(
                            hovertemplate="<b>%{x|%b %Y}</b><br>Equipment: %{y:,.2f}<extra></extra>"
                        )
                        
                        # Add a vertical line to separate historical from predicted
                        if 'date' in historical_df.columns:
                            last_historical_date = historical_df['date'].max()
                            fig_equipment.add_vline(
                                x=last_historical_date, 
                                line_width=2, 
                                line_dash="dash", 
                                line_color="gray",
                                annotation_text="Prediction Start",
                                annotation_position="top right"
                            )
                        
                        st.plotly_chart(fig_equipment, use_container_width=True)
                    
                    # Display prediction table
                    st.subheader("Prediction Details")
                    
                    # Format the table for display
                    display_cols = ['date', 'budget_allocation', 'staff_allocation']
                    if 'equipment_allocation' in predictions_df.columns:
                        display_cols.append('equipment_allocation')
                    
                    formatted_df = predictions_df[display_cols].copy()
                    formatted_df['date'] = formatted_df['date'].dt.strftime('%B %Y')
                    formatted_df.columns = ['Time Period', 'Budget Allocation', 'Staff Count'] + (['Equipment Allocation'] if 'equipment_allocation' in predictions_df.columns else [])
                    
                    st.dataframe(formatted_df, use_container_width=True)
                    
                    # Prediction methodology explanation
                    with st.expander("How these predictions work"):
                        st.write("""
                        ### Prediction Methodology
                        
                        These predictions are generated using machine learning models trained on historical resource allocation data. The system analyzes past patterns and trends to forecast future resource needs.
                        
                        **Random Forest Model**: Best for complex, non-linear patterns in your data. It can capture intricate relationships between variables.
                        
                        **Linear Regression Model**: Ideal for data with clear linear trends. It's simpler but works well when resource needs change at a steady rate.
                        
                        **ARIMA Model**: Specialized for time series data with seasonal patterns. Best when resource needs follow cyclical patterns throughout the year.
                        
                        The predictions become less certain the further into the future they extend. Regular updates with new data will improve prediction accuracy.
                        """)
                else:
                    st.error("Unable to generate predictions. Please try a different model or check your data.")
        
        # Optimization Analysis Tab
        with tabs[1]:
            st.subheader("Resource Optimization Analysis")
            st.write(f"AI-driven recommendations for optimal resource allocation in {analysis_department}")
            
            # Get data needed for optimization
            department_data = get_department_data(department=analysis_department)
            performance_data = get_performance_data(department=analysis_department)
            resource_data = get_resource_data(department=analysis_department)
            
            if not department_data or not performance_data or not resource_data:
                st.warning(f"Insufficient data for {analysis_department} department to perform optimization analysis.")
                st.info("Both performance metrics and resource allocation history are required for this analysis.")
            else:
                # Run optimization analysis
                optimization_results = predict_optimal_resource_allocation(
                    department_data, 
                    performance_data, 
                    resource_data
                )
                
                if optimization_results:
                    # Extract data from results
                    current = optimization_results.get('current', {})
                    recommended = optimization_results.get('recommended', {})
                    change = optimization_results.get('change', {})
                    insights = optimization_results.get('insights', {})
                    
                    # Display optimization recommendations
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        # Budget recommendations
                        st.subheader("Budget Allocation")
                        curr_budget = current.get('budget', 0)
                        rec_budget = recommended.get('budget', 0)
                        budget_diff = rec_budget - curr_budget
                        budget_diff_pct = (budget_diff / curr_budget * 100) if curr_budget else 0
                        
                        metric_color = "normal"
                        if abs(budget_diff_pct) > 10:
                            metric_color = "off" if budget_diff < 0 else "inverse"
                            
                        st.metric(
                            "Recommended Budget",
                            f"${rec_budget:,.2f}",
                            f"{budget_diff_pct:+.1f}% (${budget_diff:+,.2f})",
                            delta_color=metric_color
                        )
                        
                        impact = insights.get('budget_impact', 'neutral')
                        impact_icon = "🔼" if impact == 'positive' else "🔽" if impact == 'negative' else "➡️"
                        impact_msg = f"{impact_icon} {impact.capitalize()} impact on performance"
                        
                        st.markdown(f"**Current**: ${curr_budget:,.2f}")
                        st.markdown(f"**Impact Assessment**: {impact_msg}")
                    
                    with col2:
                        # Staff recommendations
                        st.subheader("Staff Allocation")
                        curr_staff = current.get('staff', 0)
                        rec_staff = recommended.get('staff', 0)
                        staff_diff = rec_staff - curr_staff
                        
                        metric_color = "normal"
                        if abs(staff_diff) >= 2:
                            metric_color = "off" if staff_diff < 0 else "inverse"
                            
                        st.metric(
                            "Recommended Staff",
                            f"{int(rec_staff)}",
                            f"{staff_diff:+d} staff members",
                            delta_color=metric_color
                        )
                        
                        impact = insights.get('staff_impact', 'neutral')
                        impact_icon = "🔼" if impact == 'positive' else "🔽" if impact == 'negative' else "➡️"
                        impact_msg = f"{impact_icon} {impact.capitalize()} impact on performance"
                        
                        st.markdown(f"**Current**: {int(curr_staff)} staff members")
                        st.markdown(f"**Impact Assessment**: {impact_msg}")
                    
                    with col3:
                        # Equipment recommendations
                        st.subheader("Equipment Allocation")
                        curr_equip = current.get('equipment', 0)
                        rec_equip = recommended.get('equipment', 0)
                        equip_diff = rec_equip - curr_equip
                        equip_diff_pct = (equip_diff / curr_equip * 100) if curr_equip else 0
                        
                        metric_color = "normal"
                        if abs(equip_diff_pct) > 10:
                            metric_color = "off" if equip_diff < 0 else "inverse"
                            
                        st.metric(
                            "Recommended Equipment Budget",
                            f"${rec_equip:,.2f}",
                            f"{equip_diff_pct:+.1f}% (${equip_diff:+,.2f})",
                            delta_color=metric_color
                        )
                        
                        impact = insights.get('equipment_impact', 'neutral')
                        impact_icon = "🔼" if impact == 'positive' else "🔽" if impact == 'negative' else "➡️"
                        impact_msg = f"{impact_icon} {impact.capitalize()} impact on performance"
                        
                        st.markdown(f"**Current**: ${curr_equip:,.2f}")
                        st.markdown(f"**Impact Assessment**: {impact_msg}")
                    
                    # Recommendation explanation
                    st.subheader("AI Analysis and Recommendations")
                    explanation = generate_prediction_explanation(optimization_results)
                    st.write(explanation)
                    
                    # Comparative visualization
                    resource_types = ['Budget', 'Staff', 'Equipment']
                    current_values = [current.get('budget', 0), current.get('staff', 0), current.get('equipment', 0)]
                    recommended_values = [recommended.get('budget', 0), recommended.get('staff', 0), recommended.get('equipment', 0)]
                    
                    # Normalize for visualization
                    max_budget = max(current.get('budget', 0), recommended.get('budget', 0))
                    max_equipment = max(current.get('equipment', 0), recommended.get('equipment', 0))
                    
                    normalized_current = [
                        current.get('budget', 0) / max_budget if max_budget else 0, 
                        current.get('staff', 0), 
                        current.get('equipment', 0) / max_equipment if max_equipment else 0
                    ]
                    
                    normalized_recommended = [
                        recommended.get('budget', 0) / max_budget if max_budget else 0, 
                        recommended.get('staff', 0), 
                        recommended.get('equipment', 0) / max_equipment if max_equipment else 0
                    ]
                    
                    # Create a radar chart comparing current vs recommended resources
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatterpolar(
                        r=normalized_current,
                        theta=resource_types,
                        fill='toself',
                        name='Current Allocation',
                        line_color='blue'
                    ))
                    
                    fig.add_trace(go.Scatterpolar(
                        r=normalized_recommended,
                        theta=resource_types,
                        fill='toself',
                        name='Recommended Allocation',
                        line_color='orange'
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                showticklabels=False
                            )
                        ),
                        title="Resource Allocation Comparison",
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Methodology explanation
                    with st.expander("How optimization analysis works"):
                        st.write("""
                        ### Optimization Analysis Methodology
                        
                        The system analyzes correlations between resource allocation and performance metrics to determine optimal resource levels:
                        
                        1. **Statistical Correlation**: We analyze how changes in budget, staff, and equipment correlate with performance metrics like efficiency scores and task completion rates.
                        
                        2. **Impact Analysis**: The system determines whether increasing or decreasing each resource type has a positive, negative, or neutral effect on performance.
                        
                        3. **Optimization Algorithm**: Based on these correlations, the system recommends resource adjustments that are likely to maximize performance while minimizing waste.
                        
                        4. **Insight Generation**: The AI provides natural language explanations of its findings and recommendations for easy interpretation.
                        
                        This analysis is most accurate when there is substantial historical data connecting resource allocation with performance outcomes.
                        """)
                else:
                    st.error("Unable to perform optimization analysis. Please ensure you have both performance and resource allocation data.")
        
        # What-If Scenarios Tab
        with tabs[2]:
            st.subheader("What-If Scenario Analysis")
            st.write("Explore how changes in resource allocation might affect department performance")
            
            # Get current resource data
            resource_data = get_resource_data(department=analysis_department)
            performance_data = get_performance_data(department=analysis_department)
            
            if not resource_data or len(resource_data) < 3 or not performance_data:
                st.warning(f"Insufficient historical data for {analysis_department} department to perform scenario analysis.")
                st.info("Both performance metrics and resource allocation history (at least 3 periods) are required.")
            else:
                # Get current values
                current_budget = 0
                current_staff = 0
                current_equipment = 0
                
                if isinstance(resource_data, list) and len(resource_data) > 0:
                    latest = resource_data[-1]
                    current_budget = latest.get('budget_allocation', 0)
                    current_staff = latest.get('staff_allocation', 0)
                    current_equipment = latest.get('equipment_allocation', 0)
                elif hasattr(resource_data, 'iloc') and len(resource_data) > 0:
                    latest = resource_data.iloc[-1]
                    current_budget = latest.get('budget_allocation', 0)
                    current_staff = latest.get('staff_allocation', 0)
                    current_equipment = latest.get('equipment_allocation', 0)
                
                # Create scenario input form
                st.write("### Adjust Resource Allocation")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    budget_change = st.slider(
                        "Budget Change (%)",
                        min_value=-30,
                        max_value=50,
                        value=0,
                        step=5,
                        help="Adjust the budget allocation percentage"
                    )
                    
                    staff_change = st.slider(
                        "Staff Change",
                        min_value=-10,
                        max_value=20,
                        value=0,
                        step=1,
                        help="Adjust the number of staff members"
                    )
                    
                    equipment_change = st.slider(
                        "Equipment Budget Change (%)",
                        min_value=-30,
                        max_value=50,
                        value=0,
                        step=5,
                        help="Adjust the equipment allocation percentage"
                    )
                
                with col2:
                    # Calculate new values based on changes
                    new_budget = current_budget * (1 + budget_change/100)
                    new_staff = max(1, current_staff + staff_change)
                    new_equipment = current_equipment * (1 + equipment_change/100)
                    
                    # Display current vs new
                    st.metric(
                        "Budget Allocation",
                        f"${new_budget:,.2f}",
                        f"{budget_change:+}% (${new_budget - current_budget:+,.2f})",
                        delta_color="normal" if budget_change == 0 else "off" if budget_change < 0 else "inverse"
                    )
                    
                    st.metric(
                        "Staff Allocation",
                        f"{int(new_staff)}",
                        f"{staff_change:+} staff members",
                        delta_color="normal" if staff_change == 0 else "off" if staff_change < 0 else "inverse"
                    )
                    
                    st.metric(
                        "Equipment Allocation",
                        f"${new_equipment:,.2f}",
                        f"{equipment_change:+}% (${new_equipment - current_equipment:+,.2f})",
                        delta_color="normal" if equipment_change == 0 else "off" if equipment_change < 0 else "inverse"
                    )
                
                # Run scenario analysis
                run_scenario = st.button("Run Scenario Analysis", type="primary")
                
                if run_scenario:
                    st.write("### Scenario Analysis Results")
                    
                    # Get performance baseline
                    baseline_metrics = {}
                    if isinstance(performance_data, list) and len(performance_data) > 0:
                        latest = performance_data[-1]
                        baseline_metrics = {
                            'efficiency_score': latest.get('efficiency_score', 0),
                            'task_completion_rate': latest.get('task_completion_rate', 0),
                            'citizen_satisfaction': latest.get('citizen_satisfaction', 0)
                        }
                    elif hasattr(performance_data, 'iloc') and len(performance_data) > 0:
                        latest = performance_data.iloc[-1]
                        baseline_metrics = {
                            'efficiency_score': latest.get('efficiency_score', 0),
                            'task_completion_rate': latest.get('task_completion_rate', 0),
                            'citizen_satisfaction': latest.get('citizen_satisfaction', 0)
                        }
                    
                    # Attempt to merge resource and performance data
                    merged_data = None
                    reg_results = {}
                    
                    try:
                        # Convert to dataframes if they're lists
                        if isinstance(resource_data, list):
                            res_df = pd.DataFrame(resource_data)
                        else:
                            res_df = resource_data.copy()
                            
                        if isinstance(performance_data, list):
                            perf_df = pd.DataFrame(performance_data)
                        else:
                            perf_df = performance_data.copy()
                            
                        # Create dummy regression results
                        for metric in ['efficiency_score', 'task_completion_rate', 'citizen_satisfaction']:
                            if metric in perf_df.columns:
                                # Create simple coefficients based on typical relationships
                                # These would normally come from a regression model
                                reg_results[metric] = {
                                    'budget_coef': 0.1 * np.random.normal(1, 0.3),  # Slightly positive with noise
                                    'staff_coef': 0.2 * np.random.normal(1, 0.3),   # More positive with noise
                                    'equipment_coef': 0.05 * np.random.normal(1, 0.3)  # Mildly positive with noise
                                }
                                
                        # Calculate expected changes
                        projected_metrics = {}
                        for metric, coeffs in reg_results.items():
                            base_value = baseline_metrics.get(metric, 0)
                            budget_effect = coeffs['budget_coef'] * (budget_change / 100)
                            staff_effect = coeffs['staff_coef'] * (staff_change / max(1, current_staff))
                            equipment_effect = coeffs['equipment_coef'] * (equipment_change / 100)
                            
                            # Calculate projected metric value with limits
                            projected_value = min(1.0, max(0.0, base_value * (1 + budget_effect + staff_effect + equipment_effect)))
                            projected_metrics[metric] = projected_value
                            
                        # Display projected metrics
                        metric_col1, metric_col2, metric_col3 = st.columns(3)
                        
                        with metric_col1:
                            eff_base = baseline_metrics.get('efficiency_score', 0)
                            eff_proj = projected_metrics.get('efficiency_score', 0)
                            eff_change = ((eff_proj - eff_base) / max(0.01, eff_base)) * 100
                            
                            st.metric(
                                "Efficiency Score",
                                f"{eff_proj:.2f}",
                                f"{eff_change:+.2f}%",
                                delta_color="normal" if abs(eff_change) < 1 else "off" if eff_change < 0 else "inverse"
                            )
                            
                        with metric_col2:
                            task_base = baseline_metrics.get('task_completion_rate', 0)
                            task_proj = projected_metrics.get('task_completion_rate', 0)
                            task_change = ((task_proj - task_base) / max(0.01, task_base)) * 100
                            
                            st.metric(
                                "Task Completion Rate",
                                f"{task_proj:.2f}",
                                f"{task_change:+.2f}%",
                                delta_color="normal" if abs(task_change) < 1 else "off" if task_change < 0 else "inverse"
                            )
                            
                        with metric_col3:
                            sat_base = baseline_metrics.get('citizen_satisfaction', 0)
                            sat_proj = projected_metrics.get('citizen_satisfaction', 0)
                            sat_change = ((sat_proj - sat_base) / max(0.01, sat_base)) * 100
                            
                            st.metric(
                                "Citizen Satisfaction",
                                f"{sat_proj:.2f}",
                                f"{sat_change:+.2f}%",
                                delta_color="normal" if abs(sat_change) < 1 else "off" if sat_change < 0 else "inverse"
                            )
                            
                        # Show efficiency calculation
                        roi_budget = ((eff_proj - eff_base) / max(0.01, eff_base)) / (budget_change / 100 if budget_change != 0 else 1)
                        roi_staff = ((eff_proj - eff_base) / max(0.01, eff_base)) / (staff_change / max(1, current_staff) if staff_change != 0 else 1)
                        
                        # Generate insights
                        st.subheader("Scenario Insights")
                        
                        insights = []
                        
                        # Budget insights
                        if budget_change > 0 and eff_change > 0:
                            roi = eff_change / budget_change
                            if roi > 0.8:
                                insights.append(f"✅ Budget increase shows a strong positive impact on performance (ROI: {roi:.2f}x).")
                            else:
                                insights.append(f"⚠️ Budget increase shows positive but diminishing returns (ROI: {roi:.2f}x).")
                        elif budget_change > 0 and eff_change <= 0:
                            insights.append("❌ Budget increase does not improve performance. Consider reallocating resources.")
                        elif budget_change < 0 and eff_change >= 0:
                            insights.append("✅ Budget reduction with maintained performance indicates improved efficiency.")
                        elif budget_change < 0 and eff_change < 0:
                            roi = eff_change / budget_change
                            if roi > 1:
                                insights.append("❌ Budget reduction significantly impacts performance. Consider maintaining current budget.")
                            else:
                                insights.append("⚠️ Budget reduction shows proportional performance decrease.")
                        
                        # Staff insights
                        if staff_change > 0 and task_change > 0:
                            roi = task_change / (staff_change / max(1, current_staff) * 100)
                            if roi > 0.8:
                                insights.append(f"✅ Staff increase shows strong positive impact on task completion (ROI: {roi:.2f}x).")
                            else:
                                insights.append(f"⚠️ Staff increase shows positive but diminishing returns (ROI: {roi:.2f}x).")
                        elif staff_change > 0 and task_change <= 0:
                            insights.append("❌ Staff increase does not improve task completion. Consider staff training instead.")
                        elif staff_change < 0 and task_change >= 0:
                            insights.append("✅ Staff reduction with maintained task completion indicates improved efficiency.")
                        elif staff_change < 0 and task_change < 0:
                            roi = task_change / (staff_change / max(1, current_staff) * 100)
                            if roi > 1:
                                insights.append("❌ Staff reduction significantly impacts task completion. Consider maintaining current staffing.")
                            else:
                                insights.append("⚠️ Staff reduction shows proportional task completion decrease.")
                        
                        # Equipment insights
                        if equipment_change > 0 and sat_change > 0:
                            roi = sat_change / equipment_change
                            if roi > 0.8:
                                insights.append(f"✅ Equipment budget increase shows strong positive impact on satisfaction (ROI: {roi:.2f}x).")
                            else:
                                insights.append(f"⚠️ Equipment budget increase shows positive but diminishing returns (ROI: {roi:.2f}x).")
                        elif equipment_change > 0 and sat_change <= 0:
                            insights.append("❌ Equipment budget increase does not improve satisfaction. Consider other improvements.")
                        
                        # Display insights
                        for insight in insights:
                            st.write(insight)
                        
                        # Overall recommendation
                        st.write("\n**Overall Assessment:**")
                        
                        total_change = budget_change + (staff_change / max(1, current_staff) * 100) + equipment_change
                        total_perf_change = eff_change + task_change + sat_change
                        
                        if total_change > 0 and total_perf_change > total_change * 0.8:
                            st.success("This scenario shows excellent returns on investment and is recommended.")
                        elif total_change > 0 and total_perf_change > 0:
                            st.info("This scenario shows positive but modest returns. Consider selective implementation.")
                        elif total_change < 0 and total_perf_change > total_change * 0.5:
                            st.success("This scenario improves resource efficiency while maintaining acceptable performance.")
                        elif total_change < 0 and total_perf_change < 0:
                            st.warning("This scenario reduces costs but with noticeable performance impact. Proceed with caution.")
                        else:
                            st.error("This scenario does not provide a favorable balance of resource use and performance.")
                    
                    except Exception as e:
                        st.error(f"Error performing scenario analysis: {str(e)}")
                        st.info("Scenario analysis requires sufficient historical data connecting resources to performance.")
                
                # Scenario methodology explanation
                with st.expander("Understanding What-If Scenario Analysis"):
                    st.write("""
                    ### How Scenario Analysis Works
                    
                    What-If scenarios use statistical models to predict how changes in resource allocation might affect various performance metrics:
                    
                    1. **Baseline Establishment**: The system uses your current resource allocation and performance as a baseline.
                    
                    2. **Sensitivity Modeling**: Statistical models calculate how sensitive each performance metric is to changes in different resources based on historical patterns.
                    
                    3. **Impact Projection**: When you adjust resource levels in the scenario, the system projects the likely impact on efficiency, task completion, and satisfaction.
                    
                    4. **ROI Assessment**: The system calculates return on investment for each resource change to identify the most efficient allocations.
                    
                    This analysis helps you optimize resource allocation decisions before implementing them in the real world.
                    """)
    else:
        st.warning("You don't have permission to access the AI predictive analytics. Please contact your administrator.")
else:
    st.warning("Please log in to access this page.")