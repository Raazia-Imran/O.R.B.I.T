import pandas as pd
import numpy as np
import os

# CONFIGURATION
FILENAME = "large_test_data.csv"
TARGET_SIZE_MB = 1000  # 1000 MB = 1 GB
CHUNK_SIZE = 500_000   # Generate 500k rows at a time to save RAM

def generate_large_csv():
    print(f"🚀 Starting generation of {TARGET_SIZE_MB}MB file...")
    
    # 1. Create a header first
    header = "Date,Region,Product,Sales,Units_Sold,Profit\n"
    with open(FILENAME, "w") as f:
        f.write(header)
    
    current_size = 0
    target_bytes = TARGET_SIZE_MB * 1024 * 1024
    
    # 2. Append data in chunks until we hit the target size
    while current_size < target_bytes:
        # Create random data
        data = {
            "Date": np.random.choice(pd.date_range('2024-01-01', periods=365), CHUNK_SIZE),
            "Region": np.random.choice(['North', 'South', 'East', 'West'], CHUNK_SIZE),
            "Product": np.random.choice(['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'], CHUNK_SIZE),
            "Sales": np.random.randint(100, 5000, CHUNK_SIZE),
            "Units_Sold": np.random.randint(1, 100, CHUNK_SIZE),
            "Profit": np.random.uniform(10.0, 500.0, CHUNK_SIZE).round(2)
        }
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Append to CSV (mode='a') without header
        df.to_csv(FILENAME, mode='a', header=False, index=False)
        
        # Check size
        current_size = os.path.getsize(FILENAME)
        print(f"📊 Current Size: {current_size / (1024*1024):.2f} MB")

    print(f"✅ DONE! File '{FILENAME}' created successfully.")

if __name__ == "__main__":
    generate_large_csv()