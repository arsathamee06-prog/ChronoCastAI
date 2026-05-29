"""
Sample Data Generator - Create realistic time series data for testing
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys

def generate_sample_data(filename='sample_timeseries.csv', rows=365):
    """
    Generate sample time series data
    
    Args:
        filename: Output CSV filename
        rows: Number of rows to generate
    """
    # Generate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=rows)
    dates = pd.date_range(start=start_date, periods=rows, freq='D')
    
    # Generate realistic time series data with trend, seasonality, and noise
    t = np.arange(rows)
    
    # Trend component
    trend = 100 + t * 0.1
    
    # Seasonal component (yearly)
    seasonality = 20 * np.sin(2 * np.pi * t / 365)
    
    # Weekly component
    weekly = 5 * np.sin(2 * np.pi * t / 7)
    
    # Random noise
    noise = np.random.normal(0, 3, rows)
    
    # Combine components
    values = trend + seasonality + weekly + noise
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'value': values,
        'volume': np.random.randint(100, 1000, rows),
        'price': np.random.uniform(50, 150, rows)
    })
    
    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Sample data generated: {filename}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {', '.join(df.columns)}")
    print(f"\nFirst few rows:")
    print(df.head())
    
    return df

if __name__ == '__main__':
    rows = int(sys.argv[1]) if len(sys.argv) > 1 else 365
    generate_sample_data(rows=rows)
