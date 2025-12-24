import pandas as pd
import numpy as np

def calculate_key_metrics(df):
    """
    Returns a dictionary of key stats.
    Handles empty data, text-only data, and logic errors gracefully.
    """
    # 1. Safety Check: Is df empty?
    if df is None or df.empty:
        return None

    # 2. Select number columns
    numeric_df = df.select_dtypes(include=[np.number])
    
    # 3. Handle "Text-Only" Files
    if numeric_df.empty:
        return None
        
    # 4. Calculate Basic Stats
    total_val = numeric_df.sum().max()  # Highest summed column (e.g., Total Sales)
    avg_val = numeric_df.mean().mean()  # Average of averages
    
    # 5. SMARTER LOGIC: Find the Real "Top Segment"
    # Old logic: Returned "Sales" (Column Name).
    # New logic: Finds the most frequent text value (e.g., "North").
    text_df = df.select_dtypes(include=['object'])
    if not text_df.empty:
        # Find the text column with the fewest unique values (likely a Category like Region)
        # We avoid ID columns which have high cardinality
        low_cardinality_cols = [col for col in text_df.columns if text_df[col].nunique() < len(df)/2]
        
        if low_cardinality_cols:
            target_col = low_cardinality_cols[0]
            top_segment = df[target_col].mode()[0] # Most frequent value (e.g., "North")
        else:
            # Fallback if all text columns are like IDs
            top_segment = "N/A"
    else:
        top_segment = "No Categories"

    summary = {
        "top_column": top_segment, 
        "total_value": total_val,
        "average_value": avg_val
    }
    return summary

def find_first_anomaly(df):
    """
    Returns the first row index and column name where a value is suspiciously low or high.
    """
    if df is None or df.empty:
        return None
        
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return None
        
    # We use Z-Score to find weird numbers (> 2.5 standard deviations)
    # Using 'fill_value=0' avoids crashing on columns with standard dev = 0
    stats = numeric_df.describe()
    std_dev = stats.loc['std']
    mean_val = stats.loc['mean']
    
    # Avoid division by zero
    std_dev = std_dev.replace(0, 1) 
    
    z_scores = np.abs((numeric_df - mean_val) / std_dev)
    outliers = (z_scores > 2.5).stack() 
    
    # Return first True value found
    anomalies = outliers[outliers]
    if not anomalies.empty:
        return anomalies.index[0] # Returns tuple: (row_index, col_name)
    return None