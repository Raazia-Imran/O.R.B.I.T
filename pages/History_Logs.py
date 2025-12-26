import streamlit as st
import pandas as pd
import sys
import os

# Connect to modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import database
from utils import ui

st.set_page_config(page_title="System Logs", layout="wide")
ui.setup_styling() 

st.title("📜 System Audit Trails")

# 1. Fetch Data
logs = database.fetch_logs()
df = pd.DataFrame(logs) if logs else pd.DataFrame(columns=["action", "user", "created_at"])

# 2a. Sidebar: Role Filter
st.sidebar.header("🔍 Filter Logs by Role")
roles = df['user'].unique().tolist() if not df.empty else []
filter_role = st.sidebar.selectbox("Select User Role", ["All"] + roles)

if filter_role != "All":
    df = df[df['user'] == filter_role]
    st.sidebar.success(f"Active Filter: {len(df)} logs")
    database.save_log(f"Filtered logs by role: {filter_role}", st.session_state.user_role)

# 2. Metrics Area
col1, col2, col3 = st.columns(3)
with col1:
    ui.card("Total Logs", str(len(df)), "System Events", "📝")
with col2:
    unique_users = df['user'].nunique() if not df.empty else 0
    ui.card("Active Users", str(unique_users), "Contributors", "👥")
with col3:
    last_event = df['created_at'].max().split("T")[1][:5] if not df.empty else "--:--"
    ui.card("Last Activity", last_event, "UTC Time", "🕒")

# 3. Search Filter
st.divider()
col_search, col_refresh = st.columns([4,1])
with col_search:
    search_term = st.text_input("🔍 Search Logs (User or Action)")
with col_refresh:
    st.write("")
    if st.button("🔄 Refresh"):
        st.rerun()

if not df.empty and search_term:
    df = df[df['action'].str.contains(search_term, case=False, na=False) |
            df['user'].str.contains(search_term, case=False, na=False)]

st.write("")

# 4. Display Table
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "created_at": st.column_config.DatetimeColumn("Timestamp", format="D MMM, HH:mm"),
        "user": "User Role",
        "action": "Activity Type"
    }
)