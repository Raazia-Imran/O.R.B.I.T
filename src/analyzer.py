"""
Module: analyzer.py
Purpose: Scalable data analysis, anomaly detection, and business insight generation
"""

import pandas as pd
import numpy as np
from typing import Dict, Any

class DataAnalyzer:
    """Analyze data and generate useful business insights"""

    def __init__(self, data:pd.DataFrame):
        """Initialize DataAnalyzer with data"""

        self.df = data.copy() #Work on a copy to preserve original data
        self._profiled = False #flag enables lazy evaluation by ensuring expensive dataset profiling operations are executed only once and cached for reuse

        self.numeric_cols = []
        self.categorical_cols = []
        self.missing_data_summary = {}
        self.numeric_data_summary = {}

    def _profile_data(self):
        """Internal method to profile the dataset"""

        if self._profiled:
            return

        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist() #Identify numeric columns
        self.categorical_cols = self.df.select_dtypes(exclude=[np.number]).columns.tolist() #Identify categorical columns
        
        self.missing_data_summary = self._compute_missing_data_summary()
        self.numeric_data_summary = self._compute_numeric_data_summary()

        self._profiled = True

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the dataset including missing data and numeric data statistics"""
        
        self._profile_data()


        return{
            "total_rows" : int(self.df.shape[0]),
            "total_columns" : int(self.df.shape[1]),
            "numeric_columns" : len(self.numeric_cols),
            "categorical_columns" : len(self.categorical_cols),
            "missing_values" : int(sum(v["count"] for v in self.missing_data_summary.values())),
            "duplicate_rows" : int(self.df.duplicated().sum()),
            "data_quality" : round(self._calculate_quality(), 2)
        }
    
    def _calculate_quality(self) -> float:
        """Calculate  data quality score based on missing values and duplicates"""

        total_cells = self.df.shape[0] * self.df.shape[1]
        
        if total_cells == 0:
            return 0.0
        
        missing_values = sum(v["count"] for v in self.missing_data_summary.values())
        return max(0.0, 1 - (missing_values / total_cells))
    
    def _compute_numeric_data_summary(self) -> Dict[str, Dict[str, Any]]:
        """Compute summary of numeric data for each column"""

        if not self.numeric_cols:
            return {}
        
        desc = self.df[self.numeric_cols].describe().T
        return{
            col: {
                "count": int(desc.loc[col, "count"]),
                "mean": float(desc.loc[col, "mean"]),
                "median": float(self.df[col].median()),
                "std": float(desc.loc[col, "std"]),
                "min": float(desc.loc[col, "min"]),
                "max": float(desc.loc[col, "max"]),
                "q1": float(desc.loc[col, "25%"]),
                "q3": float(desc.loc[col, "75%"])
            } 
            
            for col in self.numeric_cols
        }
    
    def get_numeric_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get summary statistics for numeric columns"""

        self._profile_data()
        return self.numeric_data_summary
    
    def _compute_missing_data_summary(self) -> Dict[str, Dict[str, Any]]:
        """Compute summary of missing data for each column"""

        missing_summary = self.df.isna().sum()
        missing = {}

        for column, count in missing_summary.items():
            if count > 0:
                missing[column] = {
                    "count" : int(count),
                    "percentage" : round(count / len(self.df) * 100, 2)
                }
            
        return missing
        
    def get_missing_data_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get summary of missing data for each column"""

        self._profile_data()
        return self.missing_data_summary
    
    def answer_question(self, question:str) -> str:
        """Generate answers to specific statistical questions about the data"""

        self._profile_data()
        q = question.lower()

        if "how many" in q or "records" in q:
            return f"The dataset contains {len(self.df):,} records."

        if "summary" in q:
            return str(self.get_summary())

        if "missing" in q:
            return "No missing values found." if not self._missing_data_summary else str(self._missing_summary)

        if "average" in q or "mean" in q:
            return str(self.get_numeric_summary())

        return "I can answer questions about records, summaries, averages, and missing data."

if __name__ == "__main__":

    import pandas as pd
    from analyzer import DataAnalyzer

    df = pd.DataFrame({
        "Sales": [100, 150, 200, None],
        "Customers": [10, 15, 20, 25],
        "Region": ["North", "South", "North", "East"]
    })

    analyzer = DataAnalyzer(df)

    print(analyzer.get_summary())
    print(analyzer.get_numeric_summary())
    print(analyzer.get_missing_data_summary())
    print(analyzer.answer_question("How many records?"))