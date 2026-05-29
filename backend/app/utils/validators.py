"""
Data validation utilities
"""
import re
import pandas as pd
from datetime import datetime

def validate_csv_file(file):
    """Validate uploaded CSV file"""
    if not file or file.filename == '':
        return False, "No file provided"
    
    if not file.filename.endswith('.csv'):
        return False, "File must be CSV format"
    
    try:
        df = pd.read_csv(file)
        if df.empty:
            return False, "CSV file is empty"
        if len(df) < 10:
            return False, "CSV file must have at least 10 rows"
        return True, df
    except Exception as e:
        return False, f"Error reading CSV: {str(e)}"

def validate_forecast_params(forecast_horizon, test_size=0.2, validation_size=0.1):
    """Validate forecast parameters"""
    errors = []
    
    if not isinstance(forecast_horizon, (int, float)) or forecast_horizon <= 0:
        errors.append("Forecast horizon must be a positive number")
    
    if not 0 < test_size < 1:
        errors.append("Test size must be between 0 and 1")
    
    if not 0 < validation_size < 1:
        errors.append("Validation size must be between 0 and 1")
    
    return len(errors) == 0, errors

def validate_date_column(df, column_name):
    """Validate if column contains valid dates"""
    try:
        pd.to_datetime(df[column_name])
        return True, "Valid date column"
    except Exception as e:
        return False, f"Invalid date column: {str(e)}"

def validate_numeric_column(df, column_name):
    """Validate if column contains numeric values"""
    try:
        pd.to_numeric(df[column_name], errors='coerce')
        if df[column_name].isnull().all():
            return False, "Column contains no numeric values"
        return True, "Valid numeric column"
    except Exception as e:
        return False, f"Invalid numeric column: {str(e)}"
