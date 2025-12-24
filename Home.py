import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("HF_API_TOKEN")

# 1. Global Page Config
st.set_page_config(
    page_title="Enterprise AI Workflow",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚀 Enterprise Data Hub")
st.markdown("### Upload Data Once, Analyze Everywhere")

# --- FIX: INITIALIZE SESSION STATE ---
# This was missing! It creates the empty variables when the app starts.
if "df" not in st.session_state:
    st.session_state.df = None
if "file_name" not in st.session_state:
    st.session_state.file_name = None

# 2. Reset Logic (Clears memory when new file uploaded)
def reset_state():
    st.session_state.df = None
    st.session_state.file_name = None

# 3. File Uploader
uploaded_file = st.file_uploader(
    "📂 Upload Dataset (CSV)", 
    type=["csv"], 
    on_change=reset_state
)

# 4. Smart Data Loading
if uploaded_file is not None:
    try:
        # 2GB Limit Check
        FILE_SIZE_LIMIT = 200 * 1024 * 1024
        
        if uploaded_file.size > FILE_SIZE_LIMIT:
            st.warning(f"⚠️ Large file detected ({uploaded_file.size / (1024*1024):.1f} MB). Loading sample for speed.")
            df = pd.read_csv(uploaded_file, nrows=10000)
        else:
            df = pd.read_csv(uploaded_file)
            
        # Save to Session State
        st.session_state.df = df
        st.session_state.file_name = uploaded_file.name
        
        st.success(f"✅ Data Loaded Successfully: {len(df)} rows.")
        st.info("👈 Please select a Portal from the Sidebar to begin analysis.")
        
    except Exception as e:
        st.error(f"❌ Error loading file: {e}")

# 5. Welcome Message
if st.session_state.df is None:
    st.info("👋 Welcome! Please upload a CSV file to unlock the Manager and Analyst portals.")