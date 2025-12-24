import streamlit as st

def setup_styling():
    """
    Injects the 'Marine Hub' (Zinc/Shadcn) styling.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #09090b;
            background-color: #ffffff;
        }

        /* Metric Cards */
        div[data-testid="stMetric"], div.stDataFrame, div.stPlotlyChart {
            background-color: #ffffff;
            border: 1px solid #e4e4e7;
            border-radius: 0.5rem;
            padding: 1.5rem;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        }
        
        /* Buttons */
        div.stButton > button {
            background-color: #18181b;
            color: #fafafa;
            border-radius: 0.375rem;
            border: 1px solid #18181b;
            padding: 0.5rem 1rem;
            font-weight: 500;
        }
        div.stButton > button:hover {
            background-color: #27272a;
            border-color: #27272a;
            transform: translateY(-1px);
        }
        
        /* Custom Text Card Container */
        .marine-card {
            border: 1px solid #e4e4e7;
            border-radius: 0.5rem;
            padding: 1.5rem;
            background-color: #f8fafc; /* Zinc-50 */
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def card(title, value, sub_text, icon="📊"):
    """
    FOR METRICS ONLY (Big Numbers)
    """
    st.markdown(f"""
    <div style="
        border: 1px solid #e4e4e7;
        border-radius: 0.5rem;
        padding: 1.25rem;
        background: white;
        box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-size: 0.875rem; font-weight: 500; color: #71717a;">{title}</span>
            <span style="font-size: 1rem; color: #71717a;">{icon}</span>
        </div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #09090b; letter-spacing: -0.05em;">
            {value}
        </div>
        <div style="font-size: 0.75rem; color: #71717a; margin-top: 0.25rem;">
            {sub_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

def text_card(title, content):
    """
    FOR LONG TEXT (Fixes the Asterisk/* bug)
    We use a container so Markdown renders perfectly.
    """
    with st.container():
        st.markdown(f"""
        <div style="
            display: flex; 
            align-items: center; 
            gap: 8px; 
            margin-bottom: 8px;
            padding-bottom: 8px;
            border-bottom: 1px solid #e4e4e7;
        ">
            <span style="font-size: 1.2rem;">📝</span>
            <span style="font-size: 0.9rem; font-weight: 600; color: #18181b;">{title}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # THIS IS THE FIX: Render content as native Streamlit Markdown
        st.markdown(content)
        
        # Add a small spacer/divider at the bottom
        st.markdown("<hr style='margin: 10px 0; border: 0; border-top: 1px solid #e4e4e7;'>", unsafe_allow_html=True)