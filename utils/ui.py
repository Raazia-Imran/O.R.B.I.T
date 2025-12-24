import streamlit as st

def setup_styling():
    """
    Injects the 'Marine Hub' (Zinc/Shadcn) styling and sets up the Logo.
    """
    # 1. Modern Sidebar & Global Tweaks
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Metric Cards - Hover Effects */
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #e4e4e7; /* Zinc-200 */
            border-radius: 0.75rem;
            padding: 1rem;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            transition: all 0.2s ease-in-out;
        }
        div[data-testid="stMetric"]:hover {
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border-color: #d4d4d8;
        }

        /* Buttons - Zinc 900 Style */
        div.stButton > button {
            background-color: #18181b;
            color: #fafafa;
            border-radius: 0.5rem;
            border: 1px solid #18181b;
            padding: 0.5rem 1.2rem;
            font-weight: 500;
            transition: all 0.2s;
        }
        div.stButton > button:hover {
            background-color: #27272a;
            border-color: #27272a;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        /* Sidebar Clean Up */
        section[data-testid="stSidebar"] {
            border-right: 1px solid #e4e4e7;
        }
        
        /* Headers */
        h1, h2, h3 {
            letter-spacing: -0.025em;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # 2. Add Logo 
    try:
        st.logo(
            image="https://cdn-icons-png.flaticon.com/512/2585/2585188.png", # Placeholder Pro Logo
            link="https://www.streamlit.io",
            icon_image=None
        )
    except:
        pass

def card(title, value, sub_text, icon="📊"):
    """
    Renders a Metric Card with the Marine Design System.
    """
    st.markdown(f"""
    <div style="
        border: 1px solid #e4e4e7;
        border-radius: 0.75rem;
        padding: 1.5rem;
        background: white;
        box-shadow: 0 1px 3px 0 rgba(0,0,0,0.02);
        margin-bottom: 1rem;
        height: 100%;
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
            <span style="font-size: 0.875rem; font-weight: 500; color: #71717a;">{title}</span>
            <span style="font-size: 1.25rem; background: #f4f4f5; padding: 6px; border-radius: 6px;">{icon}</span>
        </div>
        <div style="font-size: 1.75rem; font-weight: 700; color: #09090b; letter-spacing: -0.03em; margin-top: 4px;">
            {value}
        </div>
        <div style="font-size: 0.80rem; color: #71717a; margin-top: 0.5rem; font-weight: 400;">
            {sub_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

def text_card(title, content):
    """
    Renders a Content Card for AI text.
    """
    with st.container():
        st.markdown(f"""
        <div style="
            background-color: #fcfcfc;
            border: 1px solid #e4e4e7;
            border-radius: 0.75rem;
            padding: 1.25rem;
            margin-bottom: 1rem;
        ">
            <div style="
                display: flex; 
                align-items: center; 
                gap: 10px; 
                margin-bottom: 12px;
                padding-bottom: 12px;
                border-bottom: 1px solid #f4f4f5;
            ">
                <span style="font-size: 1.1rem;">✨</span>
                <span style="font-size: 0.95rem; font-weight: 600; color: #18181b;">{title}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Native Markdown Rendering
        st.markdown(content)
        
        st.markdown("</div>", unsafe_allow_html=True)