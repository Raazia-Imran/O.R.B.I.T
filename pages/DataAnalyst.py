import streamlit as st
import sys
import os

# --- CONNECTING TO Waheeba's CODE (SRC) ---
# This line allows us to import from the 'src' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# NOW we can import the Lead's files
from src.analyzer import DataAnalyzer
from src.data_processor import DataProcessor

st.title("🔬 Analyst Workbench")

if "df" not in st.session_state or st.session_state.df is None:
    st.warning("⚠️ Please upload data on the Home Page first.")
else:
    st.write("✅ Data Received from Home Page.")
    
    # TODO: Teammate B - Add your cleaning logic here using DataProcessor
    st.info("🛠️ This page is under construction. Features to add: Data Cleaning, Deep Statistics.")