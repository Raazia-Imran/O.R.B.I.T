
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_processor import DataProcessor

def perform_advanced_cleaning(uploaded_file):
    """
    Uses to clean data.
    """
    # Initialize class
    processor = DataProcessor()
    
    # Load and Clean
    # (save the uploaded file temporarily because code expects a path)
    temp_path = "temp_upload.csv"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    processor.load_data(temp_path)
    cleaned_df = processor.clean_data()
    
    # Get stats using
    info = processor.get_info()
    
    return cleaned_df, info