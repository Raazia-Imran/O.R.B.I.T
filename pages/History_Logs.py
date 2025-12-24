# # pages/History_Logs.py
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))

# import streamlit as st
# import pandas as pd
# from database import fetch_logs_df

# SUPABASE_URL = st.secrets["SUPABASE_URL"]
# SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# # Page configuration
# st.set_page_config(page_title="History Logs", layout="wide")
# st.title("History Logs")

# # Fetch logs from backend
# logs_df = fetch_logs_df()

# # Check if there are any logs
# if logs_df.empty:
#     st.info("No logs yet.")
# else:
#     # Convert timestamp to datetime and sort
#     logs_df["created_at"] = pd.to_datetime(logs_df["created_at"])
#     logs_df = logs_df.sort_values("created_at", ascending=False)

#     # Optional: Filter by user
#     user_filter = st.selectbox("Filter by user", options=["All"] + logs_df["user"].unique().tolist())
    
#     if user_filter != "All":
#         filtered_df = logs_df[logs_df["user"] == user_filter]
#     else:
#         filtered_df = logs_df

#     # Display only the filtered table
#     st.dataframe(
#         filtered_df[["user", "action", "created_at"]],
#         use_container_width=True
#     )


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
logs = database.fetch_logs() # Returns a list of dicts
if logs:
    df = pd.DataFrame(logs)
else:
    df = pd.DataFrame(columns=["action", "user", "created_at"])

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

# 3. Search & Filter
st.divider()
col_search, col_refresh = st.columns([4,1])
with col_search:
    search_term = st.text_input("🔍 Search Logs (User or Action)")
with col_refresh:
    if st.button("🔄 Refresh"):
        st.rerun()

# 4. Filter Logic
if not df.empty and search_term:
    df = df[df['action'].str.contains(search_term, case=False) | df['user'].str.contains(search_term, case=False)]

# 5. Professional Table
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