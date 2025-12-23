"""
Module: data_processor.py
Purpose: Load and clean data from files
"""

import pandas as pd
import numpy as np

class DataProcessor:
     """Load and process data files"""

     def __init__(self):
          """Initialize DataProcessor"""
          self.data = None
          self.original_file = None

     def load_data(self, file_path):
               """Load data from CSV or Excel file"""

               try:
                    if file_path.endswith(".csv"):
                         self.data = pd.read_csv(file_path)
                    
                    elif file_path.endswith(("xlsx","xls")):
                         self.data = pd.read_excel(file_path)

                    else:
                         raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
                    
                     # Keep original for comparison
                    self.original_file = self.data.copy()

                    print(f"rows : {self.data.shape[0]}\ncolumns: {self.data.shape[1]}")
                    return self.data
               
               except Exception as e:
                    print(f"Error loading data : {e}")
                    raise
            
     def clean_data(self):
               """Clean the loaded data by handling empty rows and columns, duplicates and reset index"""

               if self.data is None:
                    raise ValueError("No data found. Please load the data first.")
               
               #Remove completey empty rows and columns

               self.data = self.data.dropna(how="all", axis = 0) #rows

               self.data = self.data.dropna(how="all", axis = 1) #columns

               #Remove duplicates

               dup_before = len(self.data)
               self.data = self.data.drop_duplicates()
               dup_after = len(self.data)

               removed = dup_before - dup_after

               #Reset index
               self.data = self.data.reset_index(drop=True)

               print(f"Data cleaned. Removed {removed} duplicate rows.")
               return self.data
          
     def get_info(self):
               """Get information about the data"""

               if self.data is None:
                    raise ValueError("No data found. Lease load the data first.")
               
               return{
                    "rows" : self.data.shape[0],
                    "columns" : self.data.shape[1],
                    "missing values" : self.data.isnull().sum().sum(),
                    "duplicate rows" : self.data.duplicated().sum(),
                    "memory usage (MB)" : self.data.memory_usage(deep=True).sum()/(1024**2)
               }

#Testing the DataProcessor class

if __name__ == "__main__":
     # Create sample data
    import os
    
    # Create sample CSV
    sample_data = pd.DataFrame({
        'Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'Sales': [100, 150, 200],
        'Region': ['North', 'South', 'East']
    })

    sample_csv_path = 'sample_data.csv'
    sample_data.to_csv(sample_csv_path, index=False)

    #Test Processor
    processor = DataProcessor()
    data = processor.load_data(sample_csv_path)

    print(f"Loaded Data:\n{data}\n")

    cleaned_data = processor.clean_data()

    print(f"Cleaned Data:\n{cleaned_data}\n")

    info = processor.get_info()

    print(f"Data Info:\n{info}\n")


               