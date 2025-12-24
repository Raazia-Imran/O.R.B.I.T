from supabase import create_client
from datetime import datetime
import pandas as pd
import streamlit as st

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_log(action, user):
    try:
        supabase.table("history_logs").insert({
            "user": user,
            "action": action,
            "created_at": datetime.now().isoformat()

        }).execute()
    except Exception as e:
        print("Error saving log:", e)

def fetch_logs():
    response = (
        supabase
        .table("history_logs")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return response.data

def fetch_logs_df():
    return pd.DataFrame(fetch_logs())
