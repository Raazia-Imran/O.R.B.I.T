import streamlit as st
import pandas as pd
import sys
import os

# --- CONNECT TO MODULES ---
# This ensures we can import from the parent 'modules' and 'utils' folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import database
from utils import ui

# 1. SETUP
# Uses favicon.svg for the browser tab logo
st.set_page_config(page_title="ORBIT | Audit", layout="wide", page_icon="favicon.svg")

# Apply ORBIT Visuals (Gradient Sidebar, Fonts)
ui.setup_styling()

st.title("📜 System Audit Trails")

# 2. FETCH REAL DATA
try:
    # Fetch raw logs from Supabase
    logs = database.fetch_logs()
except Exception as e:
    st.error(f"❌ Database Connection Error: {e}")
    logs = []

# 3. METRICS SECTION (Calculated from Real Data)
if logs:
    df_logs = pd.DataFrame(logs)
    
    # -- Metric 1: Total Events --
    total_logs = len(df_logs)
    
    # -- Metric 2: Active Roles (Count Unique Users) --
    if 'user_role' in df_logs.columns:
        active_users = df_logs['user_role'].nunique()
    else:
        active_users = 1 
        
    # -- Metric 3: Last Activity Time --
    if 'created_at' in df_logs.columns and not df_logs.empty:
        # Convert string timestamp to datetime object
        df_logs['created_at'] = pd.to_datetime(df_logs['created_at'])
        # Get the latest time
        last_active = df_logs['created_at'].max().strftime("%H:%M")
    else:
        last_active = "--:--"

    # Display ORBIT Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        ui.card("Total Events", f"{total_logs}", "System Actions", "📝")
    with col2:
        ui.card("Active Roles", f"{active_users}", "Unique Accessors", "👥")
    with col3:
        ui.card("Last Sync", f"{last_active}", "UTC Time", "🕒")

    st.divider()
    
    # 4. SEARCH & TABLE
    st.markdown("### 🔍 Search Log History")
    search_term = st.text_input("Filter logs...", placeholder="Type 'Manager', 'Upload', or 'Error'...")
    
    # Search Logic
    if search_term:
        # Search across all columns
        mask = df_logs.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
        df_display = df_logs[mask]
    else:
        df_display = df_logs
        
    # Display Professional Table
    st.dataframe(
        df_display, 
        use_container_width=True,
        hide_index=True,
        column_config={
            "created_at": st.column_config.DatetimeColumn(
                "Timestamp",
                format="D MMM, HH:mm:ss"
            ),
            "action": "Activity Performed",
            "user_role": st.column_config.TextColumn(
                "User Role",
                help="The permission level of the user who performed the action"
            ),
            "details": "Metadata / Notes"
        }
    )

else:
    st.info("ℹ️ No audit logs found in the database yet. Go to the Manager or Analyst portal and perform actions to generate logs.")