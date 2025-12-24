import streamlit as st
import pandas as pd
import time
from utils import ui 

# 1. Config & Styling
st.set_page_config(page_title="Enterprise AI Hub", layout="wide", page_icon="🚀")
ui.setup_styling()

# 2. Hero Section (Modern Layout)
# We use a container to center the visual weight
with st.container():
    st.title("Enterprise AI Nexus")
    st.markdown("""
        <p style='font-size: 1.25rem; color: #52525b; max-width: 600px; line-height: 1.6;'>
            Transform raw data into <b>Strategic Intelligence</b>. 
            Upload your system logs to activate the autonomous agent workflow.
        </p>
    """, unsafe_allow_html=True)

st.divider()

# 3. Main Action Area
col_upload, col_status = st.columns([2, 1], gap="large")

with col_upload:
    st.subheader("📂 Ingest Data")
    
    # State Management
    if "df" not in st.session_state:
        st.session_state.df = None
        st.session_state.file_name = None

    def reset_state():
        st.session_state.df = None

    uploaded_file = st.file_uploader(
        "Upload CSV System Logs", 
        type=["csv"], 
        on_change=reset_state,
        help="Max file size: 2GB. Larger files will be sampled."
    )

with col_status:
    st.subheader("🖥️ System Health")
    # Using the new card design
    ui.card("AI Engine", "Online", "Model: Qwen-72B / Phi-3", "🟢")
    
# 4. Processing Logic
if uploaded_file:
    try:
        # File Handling Logic
        if uploaded_file.size > 200 * 1024 * 1024:
            st.warning("⚠️ Large file detected. Auto-sampling 10k rows for performance.")
            df = pd.read_csv(uploaded_file, nrows=10000)
        else:
            df = pd.read_csv(uploaded_file)

        st.session_state.df = df
        st.session_state.file_name = uploaded_file.name
        
        # Success Animation
        st.success(f"✅ Successfully ingested {len(df):,} records.")
        
        # Visual Progress Bar
        progress_text = "Initializing Manager Portal..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        
        st.info("🚀 Data Ready. Navigate to **Manager Portal** in the sidebar.")

    except Exception as e:
        st.error(f"Ingestion Error: {e}")