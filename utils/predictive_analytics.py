import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA

def prepare_historical_data(resource_data):
    """
    Prepares historical resource allocation data for predictive modeling.
    
    Parameters:
    - resource_data: DataFrame containing historical resource allocation data
    
    Returns:
    - DataFrame with features engineered for prediction
    """
    if resource_data is None or len(resource_data) < 3:
        return None
    
    # Convert to dataframe if it's a list of dictionaries
    if isinstance(resource_data, list):
        df = pd.DataFrame(resource_data)
    else:
        df = resource_data.copy()
    
    # Ensure we have date information
    if 'year' in df.columns and 'month' in df.columns:
        # Create date column for time series analysis
        df['date'] = df.apply(lambda x: pd.Timestamp(year=int(x['year']), month=int(x['month']), day=1), axis=1)
        df = df.sort_values('date')
    
    # Calculate additional features
    if 'budget_allocation' in df.columns and 'staff_allocation' in df.columns:
        df['budget_per_staff'] = df['budget_allocation'] / df['staff_allocation'].clip(lower=1)
    
    # Calculate rolling averages
    if len(df) >= 3:
        df['budget_rolling_avg'] = df['budget_allocation'].rolling(window=3, min_periods=1).mean()
        df['staff_rolling_avg'] = df['staff_allocation'].rolling(window=3, min_periods=1).mean()
    
    # Handle missing values
    df = df.fillna(df.mean())
    
    return df

def predict_resource_needs(historical_data, prediction_periods=3, model_type='random_forest'):
    """
    Predicts future resource needs based on historical data.
    
    Parameters:
    - historical_data: DataFrame containing prepared historical data
    - prediction_periods: Number of periods (months) to predict
    - model_type: Type of model to use ('linear', 'random_forest', 'arima')
    
    Returns:
    - DataFrame containing predicted resource needs
    """
    if historical_data is None or len(historical_data) < 3:
        return None
    
    df = prepare_historical_data(historical_data)
    
    if df is None or len(df) < 3:
        return None
    
    # Get the last date in the dataset
    last_date = df['date'].max()
    department = df['department'].iloc[0] if 'department' in df.columns else 'Unknown'
    
    # Create future dates for prediction
    future_dates = [last_date + pd.DateOffset(months=i+1) for i in range(prediction_periods)]
    
    # For budget prediction
    predictions_budget = []
    predictions_staff = []
    predictions_equipment = []
    
    # Use different model types based on parameter
    if model_type == 'arima':
        # ARIMA model for time series prediction
        try:
            # Budget prediction
            if 'budget_allocation' in df.columns:
                model_budget = ARIMA(df['budget_allocation'].values, order=(1, 1, 0))
                model_fit_budget = model_budget.fit()
                budget_forecast = model_fit_budget.forecast(steps=prediction_periods)
                predictions_budget = budget_forecast.tolist()
            
            # Staff prediction
            if 'staff_allocation' in df.columns:
                model_staff = ARIMA(df['staff_allocation'].values, order=(1, 1, 0))
                model_fit_staff = model_staff.fit()
                staff_forecast = model_fit_staff.forecast(steps=prediction_periods)
                predictions_staff = [max(round(x), 1) for x in staff_forecast.tolist()]
            
            # Equipment prediction
            if 'equipment_allocation' in df.columns:
                model_equipment = ARIMA(df['equipment_allocation'].values, order=(1, 1, 0))
                model_fit_equipment = model_equipment.fit()
                equipment_forecast = model_fit_equipment.forecast(steps=prediction_periods)
                predictions_equipment = equipment_forecast.tolist()
                
        except Exception as e:
            print(f"ARIMA model error: {e}")
            # Fallback to linear regression
            model_type = 'linear'
    
    if model_type in ['linear', 'random_forest']:
        # Prepare features - use time as the main feature
        if 'date' in df.columns:
            df['days_since_start'] = (df['date'] - df['date'].min()).dt.days
            X = df[['days_since_start']]
            
            # Add more features if available
            feature_columns = ['days_since_start']
            if 'budget_rolling_avg' in df.columns:
                feature_columns.append('budget_rolling_avg')
            if 'staff_rolling_avg' in df.columns:
                feature_columns.append('staff_rolling_avg')
            
            X = df[feature_columns]
            
            # Future X values
            future_days = [(date - df['date'].min()).days for date in future_dates]
            X_future = pd.DataFrame({'days_since_start': future_days})
            
            # For other features in future prediction, use the last value
            for col in feature_columns:
                if col != 'days_since_start':
                    X_future[col] = df[col].iloc[-1]
            
            # Budget prediction
            if 'budget_allocation' in df.columns:
                y_budget = df['budget_allocation']
                
                if model_type == 'linear':
                    model_budget = make_pipeline(StandardScaler(), Ridge(alpha=1.0))
                else:  # random_forest
                    model_budget = RandomForestRegressor(n_estimators=100, random_state=42)
                
                model_budget.fit(X, y_budget)
                predictions_budget = model_budget.predict(X_future).tolist()
            
            # Staff prediction
            if 'staff_allocation' in df.columns:
                y_staff = df['staff_allocation']
                
                if model_type == 'linear':
                    model_staff = make_pipeline(StandardScaler(), Ridge(alpha=1.0))
                else:  # random_forest
                    model_staff = RandomForestRegressor(n_estimators=100, random_state=42)
                
                model_staff.fit(X, y_staff)
                staff_pred = model_staff.predict(X_future)
                predictions_staff = [max(round(x), 1) for x in staff_pred.tolist()]
            
            # Equipment prediction
            if 'equipment_allocation' in df.columns:
                y_equipment = df['equipment_allocation']
                
                if model_type == 'linear':
                    model_equipment = make_pipeline(StandardScaler(), Ridge(alpha=1.0))
                else:  # random_forest
                    model_equipment = RandomForestRegressor(n_estimators=100, random_state=42)
                
                model_equipment.fit(X, y_equipment)
                predictions_equipment = model_equipment.predict(X_future).tolist()
    
    # Create prediction dataframe
    predictions = []
    for i, date in enumerate(future_dates):
        prediction = {
            'department': department,
            'year': date.year,
            'month': date.month,
            'date': date,
            'is_prediction': True
        }
        
        if predictions_budget and i < len(predictions_budget):
            prediction['budget_allocation'] = max(0, predictions_budget[i])
        
        if predictions_staff and i < len(predictions_staff):
            prediction['staff_allocation'] = max(1, int(round(predictions_staff[i])))
        
        if predictions_equipment and i < len(predictions_equipment):
            prediction['equipment_allocation'] = max(0, predictions_equipment[i])
        
        predictions.append(prediction)
    
    return predictions

def predict_optimal_resource_allocation(department_data, performance_data, resource_data):
    """
    Predicts optimal resource allocation based on department performance and historical data.
    
    Parameters:
    - department_data: Data about the department
    - performance_data: Historical performance metrics
    - resource_data: Historical resource allocation data
    
    Returns:
    - Dictionary with optimal resource allocation recommendations
    """
    if not department_data or not performance_data or not resource_data:
        return None
    
    try:
        # Convert to DataFrame if needed
        if isinstance(performance_data, list):
            perf_df = pd.DataFrame(performance_data)
        else:
            perf_df = performance_data.copy()
            
        if isinstance(resource_data, list):
            res_df = pd.DataFrame(resource_data)
        else:
            res_df = resource_data.copy()
        
        # Merge data if possible
        if 'date' in perf_df.columns and 'date' in res_df.columns:
            # Convert to datetime if needed
            if not pd.api.types.is_datetime64_any_dtype(perf_df['date']):
                perf_df['date'] = pd.to_datetime(perf_df['date'])
            if not pd.api.types.is_datetime64_any_dtype(res_df['date']):
                res_df['date'] = pd.to_datetime(res_df['date'])
                
            # Align the dates (use month start for matching)
            perf_df['month_start'] = perf_df['date'].dt.to_period('M').dt.to_timestamp()
            res_df['month_start'] = res_df['date'].dt.to_period('M').dt.to_timestamp()
            
            # Merge the dataframes
            merged_df = pd.merge(
                perf_df, 
                res_df, 
                left_on=['department', 'month_start'], 
                right_on=['department', 'month_start'],
                suffixes=('_perf', '_res')
            )
        else:
            # Can't merge by date, so we'll analyze them separately
            merged_df = None
            
        # Optimal resource calculation
        if merged_df is not None and len(merged_df) >= 3:
            # Analyze correlation between resources and performance
            X = merged_df[['budget_allocation', 'staff_allocation']]
            if 'equipment_allocation' in merged_df.columns:
                X['equipment_allocation'] = merged_df['equipment_allocation']
                
            # Add constant for statsmodels
            X = sm.add_constant(X)
            
            # Use different performance metrics as target
            results = {}
            
            for metric in ['efficiency_score', 'task_completion_rate', 'citizen_satisfaction']:
                if metric in merged_df.columns:
                    y = merged_df[metric]
                    
                    # OLS regression to understand impact of resources on performance
                    model = sm.OLS(y, X).fit()
                    
                    # Store coefficients
                    results[metric] = {
                        'budget_coef': model.params.get('budget_allocation', 0),
                        'staff_coef': model.params.get('staff_allocation', 0),
                        'equipment_coef': model.params.get('equipment_allocation', 0) 
                            if 'equipment_allocation' in X.columns else 0
                    }
            
            # Get current resource levels (from most recent data)
            current_budget = res_df['budget_allocation'].iloc[-1] if 'budget_allocation' in res_df.columns else 0
            current_staff = res_df['staff_allocation'].iloc[-1] if 'staff_allocation' in res_df.columns else 0
            current_equipment = res_df['equipment_allocation'].iloc[-1] if 'equipment_allocation' in res_df.columns else 0
            
            # Calculate recommended changes based on coefficients
            budget_coefficients = [results[m]['budget_coef'] for m in results]
            staff_coefficients = [results[m]['staff_coef'] for m in results]
            equipment_coefficients = [results[m]['equipment_coef'] for m in results]
            
            # Average the coefficients (with sign indicating direction)
            avg_budget_impact = sum(budget_coefficients) / len(budget_coefficients) if budget_coefficients else 0
            avg_staff_impact = sum(staff_coefficients) / len(staff_coefficients) if staff_coefficients else 0
            avg_equipment_impact = sum(equipment_coefficients) / len(equipment_coefficients) if equipment_coefficients else 0
            
            # Calculate optimal changes
            # If coefficient is positive, it means increasing this resource improves performance
            recommended_budget_change = 0.1 if avg_budget_impact > 0 else -0.05 if avg_budget_impact < 0 else 0
            recommended_staff_change = 1 if avg_staff_impact > 0 else -1 if avg_staff_impact < 0 and current_staff > 1 else 0
            recommended_equipment_change = 0.1 if avg_equipment_impact > 0 else -0.05 if avg_equipment_impact < 0 else 0
            
            # Calculate recommended values
            recommended_budget = current_budget * (1 + recommended_budget_change)
            recommended_staff = max(1, current_staff + recommended_staff_change)
            recommended_equipment = current_equipment * (1 + recommended_equipment_change)
            
            return {
                'current': {
                    'budget': current_budget,
                    'staff': current_staff,
                    'equipment': current_equipment
                },
                'recommended': {
                    'budget': recommended_budget,
                    'staff': recommended_staff,
                    'equipment': recommended_equipment
                },
                'change': {
                    'budget': recommended_budget - current_budget,
                    'budget_percent': recommended_budget_change * 100,
                    'staff': recommended_staff - current_staff,
                    'equipment': recommended_equipment - current_equipment,
                    'equipment_percent': recommended_equipment_change * 100
                },
                'insights': {
                    'budget_impact': 'positive' if avg_budget_impact > 0 else 'negative' if avg_budget_impact < 0 else 'neutral',
                    'staff_impact': 'positive' if avg_staff_impact > 0 else 'negative' if avg_staff_impact < 0 else 'neutral',
                    'equipment_impact': 'positive' if avg_equipment_impact > 0 else 'negative' if avg_equipment_impact < 0 else 'neutral',
                }
            }
        else:
            # Not enough data for correlation analysis, use simple prediction
            predictions = predict_resource_needs(resource_data, prediction_periods=1)
            
            if predictions and len(predictions) > 0:
                pred = predictions[0]
                
                return {
                    'current': {
                        'budget': resource_data[-1]['budget_allocation'] if 'budget_allocation' in resource_data[-1] else 0,
                        'staff': resource_data[-1]['staff_allocation'] if 'staff_allocation' in resource_data[-1] else 0,
                        'equipment': resource_data[-1]['equipment_allocation'] if 'equipment_allocation' in resource_data[-1] else 0
                    },
                    'recommended': {
                        'budget': pred.get('budget_allocation', 0),
                        'staff': pred.get('staff_allocation', 0),
                        'equipment': pred.get('equipment_allocation', 0)
                    },
                    'insights': {
                        'budget_impact': 'neutral',
                        'staff_impact': 'neutral',
                        'equipment_impact': 'neutral',
                    }
                }
    except Exception as e:
        print(f"Error in optimal resource prediction: {e}")
        return None
            
    return None

def generate_prediction_explanation(prediction_data):
    """
    Generates a natural language explanation of resource prediction results.
    
    Parameters:
    - prediction_data: Dictionary containing prediction results
    
    Returns:
    - String with explanation of the predictions
    """
    if not prediction_data:
        return "Insufficient data for prediction analysis."
    
    try:
        current = prediction_data.get('current', {})
        recommended = prediction_data.get('recommended', {})
        change = prediction_data.get('change', {})
        insights = prediction_data.get('insights', {})
        
        # Build explanation
        explanation = []
        
        # Budget explanation
        budget_current = current.get('budget', 0)
        budget_recommended = recommended.get('budget', 0)
        budget_change_percent = change.get('budget_percent', 0)
        budget_impact = insights.get('budget_impact', 'neutral')
        
        if budget_impact == 'positive':
            explanation.append(
                f"Budget allocation has a positive impact on performance metrics. "
                f"A {abs(budget_change_percent):.1f}% increase from {budget_current:,.2f} to {budget_recommended:,.2f} "
                f"is recommended to improve department performance."
            )
        elif budget_impact == 'negative':
            explanation.append(
                f"Budget allocation shows diminishing returns on performance. "
                f"Consider a {abs(budget_change_percent):.1f}% reduction from {budget_current:,.2f} to {budget_recommended:,.2f} "
                f"to optimize resource utilization."
            )
        else:
            explanation.append(
                f"Current budget allocation of {budget_current:,.2f} appears optimal "
                f"based on available performance data."
            )
        
        # Staff explanation
        staff_current = current.get('staff', 0)
        staff_recommended = recommended.get('staff', 0)
        staff_change = change.get('staff', 0)
        staff_impact = insights.get('staff_impact', 'neutral')
        
        if staff_impact == 'positive' and staff_change > 0:
            explanation.append(
                f"Staff allocation has a positive correlation with performance. "
                f"Consider increasing staff from {staff_current} to {staff_recommended} "
                f"to enhance department productivity."
            )
        elif staff_impact == 'negative' and staff_change < 0:
            explanation.append(
                f"Analysis suggests current staffing may be higher than optimal. "
                f"Consider adjusting staff allocation from {staff_current} to {staff_recommended} "
                f"for better resource efficiency."
            )
        else:
            explanation.append(
                f"Current staff allocation of {staff_current} appears to be within "
                f"the optimal range based on performance analysis."
            )
        
        # Equipment explanation
        equipment_current = current.get('equipment', 0)
        equipment_recommended = recommended.get('equipment', 0)
        equipment_change_percent = change.get('equipment_percent', 0)
        equipment_impact = insights.get('equipment_impact', 'neutral')
        
        if equipment_impact == 'positive':
            explanation.append(
                f"Equipment investment shows a positive impact on department performance. "
                f"A {abs(equipment_change_percent):.1f}% increase from {equipment_current:,.2f} to {equipment_recommended:,.2f} "
                f"is recommended to support operations."
            )
        elif equipment_impact == 'negative':
            explanation.append(
                f"Equipment allocation shows potential for optimization. "
                f"Consider a {abs(equipment_change_percent):.1f}% reduction from {equipment_current:,.2f} to {equipment_recommended:,.2f} "
                f"to improve resource efficiency."
            )
        else:
            explanation.append(
                f"Current equipment allocation of {equipment_current:,.2f} appears appropriate "
                f"based on performance analysis."
            )
        
        # Overall recommendation
        explanation.append(
            "These recommendations are based on statistical analysis of the relationship "
            "between resource allocation and performance metrics. Regular review of these "
            "allocations is recommended as new data becomes available."
        )
        
        return "\n\n".join(explanation)
        
    except Exception as e:
        print(f"Error generating explanation: {e}")
        return "Unable to generate detailed explanation due to insufficient data."