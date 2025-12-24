

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
import time
import urllib.parse

# --- CONNECT TO MODULES ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import database
from utils import ui, math_utils, ai_helper

# 1. SETUP & STYLING
st.set_page_config(page_title="Manager Portal", layout="wide")
ui.setup_styling()

st.title("📈 Executive Command Center")

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
        # Apply Filter
        df = df_original[df_original[filter_col] == selected_val]
        st.sidebar.success(f"Active Filter: {len(df)} rows")
    else:
        df = df_original
else:
    df = df_original

# Calculate metrics based on the FILTERED data
stats = math_utils.calculate_key_metrics(df)

# ---  FORMAT STATS FOR BETTER AI TEXT ---

formatted_stats = {
    "Total Revenue": f"${stats['total_value']:,.2f}",
    "Average Ticket": f"${stats['average_value']:,.2f}",
    "Top Segment": stats['top_column']
}

# 4. METRIC CARDS
col1, col2, col3 = st.columns(3)
with col1:
    ui.card("Total Revenue", f"{stats['total_value']:,.0f}", "Live Data", "💰")
with col2:
    ui.card("Top Segment", str(stats['top_column']), "High Activity", "🏆")
with col3:
    ui.card("Avg Ticket", f"${stats['average_value']:,.2f}", "Per Transaction", "💳")

# =========================================================
# CHARTS & TARGETS 
# =========================================================
st.markdown("### 📊 Performance Targets")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Target Gauge
    target = 1000000 
    progress = min(stats['total_value'] / target, 1.0)
    
    ui.card("Revenue Goal ($1M)", f"{progress*100:.1f}%", "Progress to Target", "🎯")
    st.progress(progress)

with chart_col2:
    if 'top_column' in stats:
        try:
            top_col_name = df.select_dtypes(include='object').columns[0]
            chart_data = df[top_col_name].value_counts().head(5)
            # Ocean Blue Color
            st.bar_chart(chart_data, color="#0ea5e9") 
        except:
            st.info("No categorical data available for chart.")

# =========================================================
#  MANDATORY 3 BUTTONS (CORE)
# =========================================================
st.divider()
st.markdown("### ⚡ AI Rapid Analysis (Core)")

b_col1, b_col2, b_col3 = st.columns(3)

# CACHING
@st.cache_data(show_spinner=False)
def fast_ai_insight(prompt):
    return ai_helper.get_llm_response(prompt)

# --- BUTTON 1: TRENDS ---
with b_col1:
    st.markdown("#### 1. Trends")
    if st.button("📊 Summarize Trends", use_container_width=True):
        t_start = time.perf_counter()
        with st.spinner("Analyzing..."):
            #  Prompt
            prompt = f"Analyze these financial stats: {formatted_stats}. Write 3 professional, business-style bullet points about the market trends. Don't mention the raw data structure."
            res = fast_ai_insight(prompt)
            
            database.save_log("Summarize Trends", "Manager")
            ui.text_card("📉 Market Trends", res)
            st.success(f"⚡ Generated in {time.perf_counter() - t_start:.2f}s")

# --- BUTTON 2: ANOMALIES ---
with b_col2:
    st.markdown("#### 2. Anomalies")
    if st.button("⚠️ Identify Anomalies", use_container_width=True):
        t_start = time.perf_counter()
        with st.spinner("Scanning..."):
            prompt = f"Look at these stats: {formatted_stats}. Identify any potential irregularities or outliers a manager should worry about. Be brief."
            res = fast_ai_insight(prompt)
            
            database.save_log("Identify Anomalies", "Manager")
            ui.text_card("🚨 Detected Anomalies", res)
            st.success(f"⚡ Generated in {time.perf_counter() - t_start:.2f}s")

# --- BUTTON 3: ACTIONS ---
with b_col3:
    st.markdown("#### 3. Actions")
    if st.button("🚀 Suggest Actions", use_container_width=True):
        t_start = time.perf_counter()
        with st.spinner("Thinking..."):
            prompt = f"Based on {formatted_stats}, suggest 3 concrete, high-impact business actions to improve revenue next month."
            res = fast_ai_insight(prompt)
            
            database.save_log("Suggest Actions", "Manager")
            ui.text_card("💡 Recommended Actions", res)
            st.success(f"⚡ Generated in {time.perf_counter() - t_start:.2f}s")

# =========================================================
# ADVANCED TOOLS (SUB CORE)
# =========================================================
st.divider()
st.markdown("### 🛠️ Advanced Executive Tools")

col_innov_1, col_innov_2 = st.columns([1, 1])

# --- VOICE COMMAND ---
with col_innov_1:
    st.info("🎤 **Voice Command Module**")
    audio_value = st.audio_input("Record strategic instruction")
    if audio_value:
        if st.button("Process Audio"):
            with st.spinner("Processing Voice Instruction..."):
                res = fast_ai_insight(f"User voice input regarding {formatted_stats}")
                ui.text_card("Voice Analysis Result", res)

# --- CEO EMAIL DRAFT (PROMPT) ---
with col_innov_2:
    st.info("✉️ **Auto-Emailer**")
    if st.button("Draft CEO Update Email", use_container_width=True):
        # Specific Prompt for Professional Format
        email_prompt = (
            f"Write a formal email to the CEO. \n"
            f"Data: {formatted_stats}. \n"
            f"Structure: Subject Line, Dear [Name], Executive Summary, Key Metrics, Conclusion. \n"
            f"Tone: Professional and concise."
        )
        res = fast_ai_insight(email_prompt)
        ui.text_card("Draft: Executive Brief", res)
        
        # Real Mailto Link
        subject = "Executive Update: Q3 Performance"
        safe_subject = urllib.parse.quote(subject)
        safe_body = urllib.parse.quote(res)
        st.link_button("🚀 Open in Outlook/Gmail", f"mailto:?subject={safe_subject}&body={safe_body}")


st.divider()
st.markdown("### 📥 Export Intelligence")

download_col1, download_col2, download_col3 = st.columns(3)

# 1. DOWNLOAD CSV (Raw Data)
with download_col1:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📄 Download Data (CSV)",
        data=csv,
        file_name="executive_data.csv",
        mime="text/csv",
        use_container_width=True
    )

# 2. DOWNLOAD REPORT (Text/Markdown)
# generate a professional text report based on the current stats
report_content = f"""
EXECUTIVE INTELLIGENCE REPORT
Generated via AI Nexus
------------------------------------------------
DATE: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

KEY METRICS:
- Total Revenue:  ${stats['total_value']:,.2f}
- Top Segment:    {stats['top_column']}
- Avg Ticket:     ${stats['average_value']:,.2f}

------------------------------------------------
STRATEGIC SUMMARY:
(See Dashboard for AI generated insights)
"""
with download_col2:
    st.download_button(
        label="📑 Download Report (TXT)",
        data=report_content,
        file_name="Executive_Summary.txt",
        mime="text/plain",
        use_container_width=True
    )

# 3. PDF / EXCEL NOTICE
with download_col3:
    # Creating real PDFs requires heavy libraries (fpdf) which might break 
    # if not in requirements.txt. We provide a 'Print Friendly' button instead.
    if st.button("🖨️ Print to PDF", use_container_width=True):
        st.toast("Press Ctrl+P (Cmd+P) and select 'Save as PDF'", icon="🖨️")
        st.balloons()