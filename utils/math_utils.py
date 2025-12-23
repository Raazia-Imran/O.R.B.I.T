import pandas as pd
import numpy as np

def calculate_key_metrics(df):
    """
    Returns a dictionary of key stats for the Trend Summary.
    """
    # Select only number columns
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return None
        
    # Fast calculations for the summary
    summary = {
        "top_column": numeric_df.sum().idxmax(),  # e.g., "Sales"
        "total_value": numeric_df.sum().max(),    # e.g., 50000
        "average_value": numeric_df.mean().mean() # e.g., 500
    }
    return summary

def find_first_anomaly(df):
    """
    Returns the first row index and column name where a value is suspiciously low or high.
    """
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return None
        
    # We use Z-Score (Standard Deviation) to find weird numbers
    # If a number is > 3 standard deviations away, it's an anomaly.
    z_scores = np.abs((numeric_df - numeric_df.mean()) / numeric_df.std())
    outliers = (z_scores > 2.5).stack() # Trigger at 2.5 sigma for demo purposes
    
    # Return first True value found
    anomalies = outliers[outliers]
    if not anomalies.empty:
        return anomalies.index[0] # Returns tuple: (row_index, col_name)
    return None