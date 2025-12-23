import streamlit as st
from utils import ai_helper
from utils import math_utils

st.title("📈 Manager Dashboard")

if "df" not in st.session_state or st.session_state.df is None:
    st.warning("⚠️ Please upload data on the Home Page first.")
else:
    st.write("✅ Data Received from Home Page.")
    
    # TODO: Teammate A - Add AI Summaries here
    st.info("🛠️ This page is under construction. Features to add: Trends, Anomalies, Actions.")