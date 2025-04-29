import pandas as pd
from datetime import datetime, timedelta
from ..config import TIME_WINDOWS

def load_data(file_path):
    """Load and process data from CSV file."""
    df = pd.read_csv(file_path)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    return df

def filter_data_by_time_window(df, time_window):
    """Filter data based on selected time window."""
    if df.empty or 'Date' not in df.columns:
        return df
    
    latest_date = df['Date'].max()
    time_ago = latest_date - timedelta(days=TIME_WINDOWS[time_window])
    return df[df['Date'] >= time_ago]

def calculate_pct_change(df):
    """Calculate percentage change for a dataframe."""
    if df.empty:
        return df
    
    df = df.sort_values('Date')
    df['pct_change'] = df['Value'].pct_change() * 100
    return df

def calculate_project_metrics(df):
    """Calculate project metrics from the dataframe."""
    if df.empty:
        return None
    
    project_metrics = df.groupby('Name').agg({
        'Value': ['mean', 'first', 'last']
    }).reset_index()
    
    project_metrics['pct_change'] = ((project_metrics[('Value', 'last')] - project_metrics[('Value', 'first')]) / 
                                   project_metrics[('Value', 'first')] * 100)
    
    project_metrics.columns = ['Project', 'Avg Devs/Month', 'First Month', 'Last Month', 'Monthly Growth %']
    project_metrics = project_metrics[['Project', 'Avg Devs/Month', 'Monthly Growth %']]
    
    return project_metrics.sort_values('Avg Devs/Month', ascending=False).head(30) 