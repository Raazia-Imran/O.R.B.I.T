import streamlit as st
import pandas as pd
import time
from utils import ui 

# 1. Config
st.set_page_config(page_title="Enterprise AI Hub", layout="wide", page_icon="🚀")
ui.setup_styling()

# 2. Hero Section
col1, col2 = st.columns([2, 1])
with col1:
    st.title("Enterprise AI Nexus")
    st.markdown("""
    <div style="color: #52525b; font-size: 18px; margin-bottom: 20px;">
    Transform raw CSV data into <b>Strategic Intelligence</b> using 
    Autonomous AI Agents.
    </div>
    """, unsafe_allow_html=True)

    # 3. File Uploader (Session State Managed)
    if "df" not in st.session_state:
        st.session_state.df = None
        st.session_state.file_name = None

    def reset_state():
        st.session_state.df = None

    uploaded_file = st.file_uploader("📂 Drop System Data (CSV)", type=["csv"], on_change=reset_state)

with col2:
    # Status Cards
    ui.card("System Status", "Online", "v2.4.0-Stable", "🟢")
    ui.card("AI Engine", "Qwen-72B", "Latency: 45ms", "🤖")

# 4. Processing Logic
if uploaded_file:
    try:
        # 2GB Logic
        if uploaded_file.size > 200 * 1024 * 1024:
            st.warning("⚠️ Large file. Loading 10k row sample.")
            df = pd.read_csv(uploaded_file, nrows=10000)
        else:
            df = pd.read_csv(uploaded_file)

        st.session_state.df = df
        st.session_state.file_name = uploaded_file.name
        
        st.success(f"✅ Ingested {len(df):,} records from {uploaded_file.name}")
        
        # Micro-interaction
        bar = st.progress(0)
        for i in range(100):
            time.sleep(0.005)
            bar.progress(i+1)
        
        st.info("👈 Select 'Manager Portal' in the sidebar to begin.")

    except Exception as e:
        st.error(f"Error: {e}")