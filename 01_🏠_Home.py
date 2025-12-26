# import streamlit as st
# import pandas as pd
# import time
# from utils import ui 

# # 1. Config
# st.set_page_config(page_title="InsightNexus AI", layout="wide", page_icon="🔮")

# # 2. Inject Styling
# ui.setup_styling()

# # 3. SPLASH SCREEN (Only runs once per session)
# if "splash_shown" not in st.session_state:
#     ui.splash_screen()
#     st.session_state.splash_shown = True

# # 4. HEADER
# with st.container():
#     st.markdown("<h1 style='text-align: center; color: #6c5ce7;'>InsightNexus AI Hub</h1>", unsafe_allow_html=True)
#     st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #636e72;'>Your Central Command for Enterprise Intelligence</p>", unsafe_allow_html=True)

# st.divider()

# # 5. MAIN NAVIGATION HUB
# col1, col2 = st.columns(2, gap="large")

# with col1:
#     st.markdown("### 📤 Upload Dataset")
    
#     # Init State
#     if "df" not in st.session_state:
#         st.session_state.df = None
#         st.session_state.file_name = None

#     uploaded_file = st.file_uploader(
#         "Drop your CSV System Logs here", 
#         type=["csv"], 
#         help="Supports files up to 2GB. Large files auto-sampled."
#     )

#     if uploaded_file:
#         try:
#             if uploaded_file.size > 200 * 1024 * 1024:
#                 st.warning("⚠️ Large file. Sampling 10k rows for speed.")
#                 df = pd.read_csv(uploaded_file, nrows=10000)
#             else:
#                 df = pd.read_csv(uploaded_file)

#             st.session_state.df = df
#             st.session_state.file_name = uploaded_file.name
            
#             st.balloons() # Playful effect on success
#             st.success(f"✅ {len(df):,} Records Ingested Successfully!")
            
#         except Exception as e:
#             st.error(f"Ingestion Failed: {e}")

# with col2:
#     st.markdown("### 🚀 Navigate to Modules")
    
#     # Navigation Cards (Using st.container for grouping)
#     with st.container():
#         st.info("Where would you like to go?")
        
#         # Grid of buttons
#         c1, c2 = st.columns(2)
#         with c1:
#             if st.button("📈 Manager Insights", use_container_width=True):
#                 st.switch_page("pages/02_📈_Manager_Insights.py")
#         with c2:
#             if st.button("🔬 Analyst Lab", use_container_width=True):
#                 st.switch_page("pages/03_🔬_Analyst_Lab.py")
                
#         if st.button("📜 View Audit Trails", use_container_width=True):
#             st.switch_page("pages/04_📜_Audit_Trails.py")

# # 6. FOOTER INFO
# st.divider()
# st.markdown("""
# <div style='text-align: center; color: #b2bec3; font-size: 0.8rem;'>
#     🔒 Secure Environment | v2.5.0 | Powered by InsightNexus Engine
# </div>
# """, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from utils import ui 
from streamlit_lottie import st_lottie

# 1. Config (Tab Title & Icon)
st.set_page_config(page_title="ORBIT", layout="wide", page_icon="favicon.svg")

# 2. Splash Screen
# NOTE IMP POINT: Streamlit clears session_state on Browser Refresh. 
# This means the Splash Screen will naturally show every time you reload the page.
if "splash_shown" not in st.session_state:
    ui.splash_screen()
    st.session_state.splash_shown = True

# 3. Styling & Logo Setup
ui.setup_styling()

# 4. Hero Section
col_text, col_anim = st.columns([1.5, 1], gap="large")

with col_text:
    st.markdown("""
        <h1 style='font-size: 4rem; font-weight: 800; background: -webkit-linear-gradient(45deg, #00f2ea, #ff00ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            O.R.B.I.T.
        </h1>
        <h3 style='color: #2d3436; margin-top: -15px;'>Operational Reporting & Business Intelligence Tool</h3>
        <p style='font-size: 1.1rem; color: #636e72; line-height: 1.6; margin-top: 20px;'>
            <b>Your Enterprise, Aligned.</b><br>
            Upload raw system logs and watch ORBIT align chaotic data into 
            clear, strategic trajectories in real-time.
        </p>
    """, unsafe_allow_html=True)
    
    # State Management
    if "df" not in st.session_state:
        st.session_state.df = None

    uploaded_file = st.file_uploader("📂 Upload Enterprise Data (CSV)", type=["csv"])

with col_anim:
    lottie_orbit = ui.load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_w51pcehl.json")
    if lottie_orbit:
        st_lottie(lottie_orbit, height=350, key="orbit_anim")
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/3212/3212567.png", width=200)

st.divider()

if uploaded_file:
    try:
        if uploaded_file.size > 200 * 1024 * 1024:
            st.warning("⚠️ Large file detected. Auto-sampling 10k rows.")
            df = pd.read_csv(uploaded_file, nrows=10000)
        else:
            df = pd.read_csv(uploaded_file)

        st.session_state.df = df
        st.success(f"✅ Orbit Established: {len(df):,} records ready for analysis.")
        
        st.markdown("### 🚀 Launch Module")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📈 Manager Insights", use_container_width=True):
                st.switch_page("pages/02_📈_Manager_Insights.py")
        with c2:
            if st.button("🔬 Analyst Lab", use_container_width=True):
                st.switch_page("pages/03_🔬_Analyst_Lab.py")
        with c3:
            if st.button("📜 Audit Trails", use_container_width=True):
                st.switch_page("pages/04_📜_Audit_Trails.py")

    except Exception as e:
        st.error(f"Ingestion Error: {e}")