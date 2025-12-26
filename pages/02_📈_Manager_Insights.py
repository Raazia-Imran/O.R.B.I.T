import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
import time
import urllib.parse
import datetime

# --- CONNECT TO MODULES ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import database
from utils import ui, math_utils, ai_helper

# 1. SETUP & STYLING
# st.set_page_config(page_title="Manager Insights", layout="wide")
st.set_page_config(page_title="ORBIT | Manager", layout="wide", page_icon="favicon.svg")
ui.setup_styling()

st.title("📈 Executive Command Center")

# --- TRUST INDICATOR ---
last_refresh = datetime.datetime.now().strftime("%H:%M:%S")
st.caption(f"🟢 System Status: Online | Last Synced: Today at {last_refresh}")

# 2. DATA SAFETY CHECK
if "df" not in st.session_state or st.session_state.df is None:
    st.warning("⚠️ Waiting for data stream. Please upload a file on the Home Page.")
    st.stop()

# =========================================================
# SIDEBAR FILTERS 
# =========================================================
df_original = st.session_state.df
st.sidebar.header("🔍 Filter Data")

categorical_cols = df_original.select_dtypes(include=['object']).columns.tolist()
if categorical_cols:
    filter_col = st.sidebar.selectbox("Filter by Category", ["All Data"] + categorical_cols)
    
    if filter_col != "All Data":
        unique_vals = df_original[filter_col].unique()
        selected_val = st.sidebar.selectbox(f"Select {filter_col}", unique_vals)
        df = df_original[df_original[filter_col] == selected_val]
        st.sidebar.success(f"Active Filter: {len(df)} rows")
    else:
        df = df_original
else:
    df = df_original

# Calculate metrics
stats = math_utils.calculate_key_metrics(df)

# --- SAFETY CHECK ---
if stats is None:
    st.error("⚠️ No numeric data found in this file.")
    st.dataframe(df.head(), use_container_width=True)
    st.stop()

# --- FORMAT STATS ---
formatted_stats = {
    "Total Revenue": f"${stats['total_value']:,.2f}",
    "Average Ticket": f"${stats['average_value']:,.2f}",
    "Top Segment": stats['top_column']
}

# 4. METRIC CARDS (Using New Prism UI)
col1, col2, col3 = st.columns(3)
with col1:
    ui.card(
        "Total Revenue", 
        f"{stats['total_value']:,.0f}", 
        "Live Data", 
        "💰",
        help_text="Sum of all transaction values in the selected filter."
    )
with col2:
    ui.card(
        "Top Segment", 
        str(stats['top_column']), 
        "High Activity", 
        "🏆",
        help_text="The category/region with the highest frequency of transactions."
    )
with col3:
    ui.card(
        "Avg Ticket", 
        f"${stats['average_value']:,.2f}", 
        "Per Transaction", 
        "💳",
        help_text="Average value per single transaction (Total Revenue / Count)."
    )

# =========================================================
# CHARTS & TARGETS 
# =========================================================
st.markdown("### 📊 Performance Targets")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # --- 🛑 FIX: CLAMP PROGRESS VALUE ---
    target = 1000000 
    raw_progress = stats['total_value'] / target
    # Ensure it stays between 0.0 and 1.0 to prevent crashes
    progress = max(0.0, min(raw_progress, 1.0))
    
    ui.card("Revenue Goal ($1M)", f"{progress*100:.1f}%", "Progress to Target", "🎯")
    st.progress(progress)

with chart_col2:
    if 'top_column' in stats:
        try:
            top_col_name = df.select_dtypes(include='object').columns[0]
            chart_data = df[top_col_name].value_counts().head(5)
            st.bar_chart(chart_data, color="#6c5ce7") # Prism Purple
        except:
            st.info("No categorical data available for chart.")

# =========================================================
# AI ANALYSIS CORE (With Skeleton Loaders)
# =========================================================
st.divider()
st.markdown("### ⚡ Instant AI Analysis")

b_col1, b_col2, b_col3 = st.columns(3, gap="medium")

@st.cache_data(show_spinner=False)
def fast_ai_insight(prompt):
    return ai_helper.get_llm_response(prompt)

# --- BUTTON 1: TRENDS ---
with b_col1:
    if st.button("📊 Summarize Trends", use_container_width=True):
        # Skeleton Loader
        placeholder = st.empty()
        with placeholder:
            ui.render_skeleton_loader()
            
        t_start = time.perf_counter()
        prompt = f"Analyze these stats: {formatted_stats}. Write 3 professional bullet points on market trends."
        res = fast_ai_insight(prompt)
        
        # Clear & Show
        placeholder.empty()
        database.save_log("Summarize Trends", "Manager")
        ui.text_card("Market Trends", res)
        st.caption(f"⚡ Generated in {time.perf_counter() - t_start:.2f}s")

# --- BUTTON 2: ANOMALIES ---
with b_col2:
    if st.button("⚠️ Detect Anomalies", use_container_width=True):
        placeholder = st.empty()
        with placeholder:
            ui.render_skeleton_loader()
            
        t_start = time.perf_counter()
        prompt = f"Check these stats for outliers: {formatted_stats}. Be brief and professional."
        res = fast_ai_insight(prompt)
        
        placeholder.empty()
        database.save_log("Identify Anomalies", "Manager")
        ui.text_card("Anomalies Detected", res)
        st.caption(f"⚡ Generated in {time.perf_counter() - t_start:.2f}s")

# --- BUTTON 3: ACTIONS ---
with b_col3:
    if st.button("🚀 Strategic Actions", use_container_width=True):
        placeholder = st.empty()
        with placeholder:
            ui.render_skeleton_loader()
            
        t_start = time.perf_counter()
        prompt = f"Based on {formatted_stats}, suggest 3 concrete business actions to improve revenue."
        res = fast_ai_insight(prompt)
        
        placeholder.empty()
        database.save_log("Suggest Actions", "Manager")
        ui.text_card("Recommended Actions", res)
        st.caption(f"⚡ Generated in {time.perf_counter() - t_start:.2f}s")

# =========================================================
# ADVANCED TOOLS
# =========================================================
st.divider()
st.markdown("### 🛠️ Advanced Executive Tools")
col_innov_1, col_innov_2 = st.columns([1, 1])

with col_innov_1:
    st.info("🎤 **Voice Command Module**")
    audio_value = st.audio_input("Record strategic instruction")
    if audio_value and st.button("Process Audio"):
        with st.spinner("Processing Voice Instruction..."):
            res = fast_ai_insight(f"User voice input regarding {formatted_stats}")
            ui.text_card("Voice Analysis Result", res)

with col_innov_2:
    st.info("✉️ **Auto-Emailer**")
    if st.button("Draft CEO Update Email", use_container_width=True):
        email_prompt = (
            f"Write a formal email to the CEO. \n"
            f"Data: {formatted_stats}. \n"
            f"Structure: Subject, Executive Summary, Key Metrics, Conclusion. \n"
            f"Tone: Professional."
        )
        res = fast_ai_insight(email_prompt)
        ui.text_card("Draft: Executive Brief", res)
        subject = urllib.parse.quote("Executive Update: Q3 Performance")
        safe_body = urllib.parse.quote(res)
        st.link_button("🚀 Open in Outlook/Gmail", f"mailto:?subject={subject}&body={safe_body}")

st.divider()
st.markdown("### 📥 Export Intelligence")
download_col1, download_col2, download_col3 = st.columns(3)

with download_col1:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📄 Download Data (CSV)", csv, "executive_data.csv", "text/csv", use_container_width=True)

with download_col2:
    report_content = f"EXECUTIVE REPORT\nDATE: {pd.Timestamp.now()}\nMETRICS: {formatted_stats}"
    st.download_button("📑 Download Report (TXT)", report_content, "Executive_Summary.txt", "text/plain", use_container_width=True)

with download_col3:
    if st.button("🖨️ Print to PDF", use_container_width=True):
        st.toast("Press Ctrl+P (Cmd+P) and select 'Save as PDF'", icon="🖨️")