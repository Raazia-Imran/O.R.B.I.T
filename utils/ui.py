import streamlit as st
import time
import base64
import requests
from streamlit_lottie import st_lottie

def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def render_svg(svg_filename):
    """Renders the SVG logo in Streamlit Sidebar"""
    try:
        with open(svg_filename, "r", encoding="utf-8") as f:
            svg_content = f.read()
        b64 = base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")
        
        # --- CHANGE 1: Increased Sidebar Logo Width to 280 ---
        html = f'<img src="data:image/svg+xml;base64,{b64}" width="280" style="margin-bottom: 20px; display: block; margin-left: auto; margin-right: auto;"/>'
        st.sidebar.markdown(html, unsafe_allow_html=True)
    except FileNotFoundError:
        st.sidebar.header("O.R.B.I.T.")

def setup_styling():
    """
    Injects the 'ORBIT' Design System & Logo.
    """
    # 1. RENDER LOGO IN SIDEBAR
    render_svg("orbit_logo.svg")

    # 2. GLOBAL CSS
    st.markdown("""
    <style>
        /* Import Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Roboto:wght@300;400;700&display=swap');
        
        /* Typography */
        h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; }
        html, body, [class*="css"], button, input { font-family: 'Roboto', sans-serif; color: #2d3436; }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
            border-right: 1px solid #dee2e6;
        }

        /* Buttons (Neon Gradient) */
        .stButton > button {
            background: linear-gradient(90deg, #0984e3, #6c5ce7);
            color: white !important;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 0 15px rgba(9, 132, 227, 0.5);
        }

        /* Metric Cards */
        div[data-testid="stMetric"] {
            background: white; border-radius: 15px; padding: 20px;
            border: 1px solid #dfe6e9;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }
        div[data-testid="stMetric"]:hover {
            transform: scale(1.02);
            border-color: #0984e3;
        }
    </style>
    """, unsafe_allow_html=True)

def splash_screen():
    """
    Displays the ORBIT Splash Screen with Fade-In effect.
    """
    empty_slot = st.empty()
    with empty_slot.container():
        # Load the SVG for the splash screen
        try:
            with open("orbit_logo.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()
            b64 = base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")
            
            # --- CHANGE 2: Increased Splash Logo Width to 500 ---
            logo_html = f'<img src="data:image/svg+xml;base64,{b64}" width="500" class="fade-in"/>'
        except:
            logo_html = "<h1>O.R.B.I.T.</h1>"

        st.markdown(f"""
        <style>
        .splash-container {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: white;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            z-index: 99999;
        }}
        .fade-in {{ animation: fadeIn 2s ease-in-out; }}
        @keyframes fadeIn {{ 0% {{ opacity: 0; transform: scale(0.9); }} 100% {{ opacity: 1; transform: scale(1); }} }}
        </style>
        
        <div class="splash-container">
            {logo_html}
            <p class="fade-in" style="font-family: 'Orbitron', sans-serif; font-size: 1.5rem; color: #b2bec3; letter-spacing: 3px; margin-top: 30px;">
                INITIALIZING CORE SYSTEMS...
            </p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(3.0) 
    
    empty_slot.empty()

def render_skeleton_loader():
    st.markdown("""
        <div style="height: 20px; width: 60%; background: #e0e0e0; border-radius: 4px; margin-bottom: 10px; animation: pulse 1.5s infinite;"></div>
        <div style="height: 15px; width: 100%; background: #f0f0f0; border-radius: 4px; margin-bottom: 5px; animation: pulse 1.5s infinite;"></div>
        <style>@keyframes pulse { 0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; } }</style>
    """, unsafe_allow_html=True)

def card(title, value, sub_text, icon="📊", help_text=None):
    tooltip_html = f"""<span title="{help_text}" style="cursor: help; color: #a29bfe; font-size: 0.8rem; margin-left: 5px;">(ℹ️)</span>""" if help_text else ""
    st.markdown(f"""
    <div style="background: white; border-radius: 15px; padding: 24px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid #f1f2f6; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <span style="font-size: 0.8rem; font-weight: 700; color: #b2bec3; text-transform: uppercase; letter-spacing: 1px;">
                    {title} {tooltip_html}
                </span>
                <div style="font-size: 2rem; font-weight: 800; color: #2d3436; margin: 5px 0;">{value}</div>
                <div style="font-size: 0.85rem; color: #0984e3; font-weight: 600;">{sub_text}</div>
            </div>
            <div style="background: #dfe6e9; color: #2d3436; width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem;">{icon}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def text_card(title, content):
    st.markdown(f"""
    <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border-left: 5px solid #00f2ea; margin-bottom: 20px;">
        <h3 style="margin: 0 0 10px 0; font-size: 1.1rem; color: #2d3436; display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 1.4rem;">🪐</span> {title}
        </h3>
        <div style="font-family: 'Roboto', sans-serif;">{content}</div>
    </div>
    """, unsafe_allow_html=True)