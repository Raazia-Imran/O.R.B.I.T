import time
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
import plotly.graph_objects as go


# --- CONNECT TO BACKEND ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.analyzer import DataAnalyzer
from src.data_processor import DataProcessor
from modules import database
from utils import ui

@st.cache_data(show_spinner=False)
def get_png_bytes(fig):
    """Return PNG bytes of a Plotly figure (cached)."""
    return fig.to_image(format="png", scale=2)

def plotly_png_download(fig, filename):
    """Creates a Streamlit download button for Plotly figures."""
    img_bytes = get_png_bytes(fig)
    return st.download_button(
        label="💾 Save as PNG",
        data=img_bytes,
        file_name=filename,
        mime="image/png",
        use_container_width=True
    )

# --- SETUP & STYLING ---
st.set_page_config(page_title="Analyst Workbench", layout="wide")
ui.setup_styling()
st.title("🔬 Analyst Workbench")

if "df" not in st.session_state or st.session_state.df is None:
    st.warning("⚠️ Please upload data on the Home Page first.")
    st.stop()

# --- CACHING ---
@st.cache_data(show_spinner=False)
def get_summary_cached(df):
    analyzer = DataAnalyzer(df)
    return analyzer.get_summary()

@st.cache_data(show_spinner=False)
def compute_corr_matrix(df, numeric_cols):
    return df[numeric_cols].corr()

@st.cache_data(show_spinner=False)
def sample_df(df, max_rows=5000):
    if len(df) > max_rows:
        return df.sample(max_rows, random_state=42)
    return df

# --- SIDEBAR FILTERS ---
df_original = st.session_state.df
st.sidebar.header("🔍 Dataset Controls")
categorical_cols = df_original.select_dtypes(include=['object']).columns.tolist()

if categorical_cols:
    filter_col = st.sidebar.selectbox("Filter Category", ["All Data"] + categorical_cols)
    if filter_col != "All Data":
        val = st.sidebar.selectbox(f"Select {filter_col}", df_original[filter_col].unique())
        df = df_original[df_original[filter_col] == val]
        st.sidebar.success(f"Filtered to {len(df)} rows")
        database.save_log(f"Filtered data by {filter_col} = {val}", "Analyst")
    else:
        df = df_original
else:
    df = df_original

# --- TOP METRICS ---
summary = get_summary_cached(df)
col1, col2, col3, col4 = st.columns(4)
with col1:
    ui.card("Data Quality", f"{summary['data_quality'] * 100:.0f}%", "Health Score", "❤️")
with col2:
    ui.card("Row Count", f"{summary['total_rows']:,}", "Filtered Rows", "📝")
with col3:
    ui.card("Duplicates", str(summary['duplicate_rows']), "Detected", "🔄")
with col4:
    ui.card("Missing Values", str(summary['missing_values']), "Cells Empty", "⚠️")

# --- DATA CLEANING ---
st.divider()
st.markdown("### 🧹 Data Cleaning Pipeline")
col_clean_action, col_clean_info = st.columns([1, 2])

with col_clean_action:
    if st.button("✨ Run Auto-Clean"):
        processor = DataProcessor()
        processor.data = df
        cleaned_df = processor.clean_data()
        st.session_state.df = cleaned_df
        database.save_log("Ran Auto-Cleaning", "Analyst")
        st.success(f"✅ Cleaned! Removed duplicates & empty rows.")
        time.sleep(1)
        st.rerun()

with col_clean_info:
    csv = df.to_csv(index=False).encode('utf-8')
    if st.download_button("💾 Download Cleaned CSV", csv, "cleaned_data.csv", "text/csv"):
        database.save_log("Downloaded cleaned CSV file", "Analyst")

# --- DEEP DIVE ANALYTICS ---
st.divider()
st.markdown("### 🔍 Deep Dive Analytics")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Distributions", "📈 Relationships", "🚨 Anomalies", "📑 Data Profiling"])

numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

# --- TAB 1: DISTRIBUTIONS ---
with tab1:
    st.markdown("#### Univariate Analysis")

    col1, col2, col3,col4 = st.columns(4)  # Correct way to create 3 columns
    with col1:
        target_col = st.selectbox("Select Column to Analyze", numeric_cols)

    col_chart, col_stats = st.columns([2, 1])

    with col_chart:

        if target_col and st.button(f"📊 Show {target_col} Distribution"):
            df_sampled = sample_df(df)
            fig = px.histogram(df_sampled, x=target_col, nbins=20, color_discrete_sequence=['#0ea5e9'], title=f"Distribution of {target_col}")
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:  # middle column

                plotly_png_download(fig, f"{target_col}_distribution.png")
                database.save_log(f"Viewed distribution for {target_col}", "Analyst")

    with col_stats:
        if target_col:
            desc = df[target_col].describe()
            st.write("") 
            st.write("") 
            st.write("") 
            st.write("") 
            st.write("**Statistical Summary**")
            st.dataframe(desc, use_container_width=True)

# --- TAB 2: RELATIONSHIPS ---
with tab2:
    st.markdown("#### Bivariate Analysis")
    col_x, col_y = st.columns(2)
    with col_x:
        x_axis = st.selectbox("X Axis", numeric_cols, index=0)
    with col_y:
        y_axis = st.selectbox("Y Axis", numeric_cols, index=min(1, len(numeric_cols)-1))

    if st.button("🔗 Generate Scatter Plot"):
        # Aggressive sampling: limit to 2k points max
        max_points = 2000
        df_sampled = df.sample(n=min(max_points, len(df)), random_state=42)

        # WebGL scatter for speed
        fig = go.Figure(go.Scattergl(
            x=df_sampled[x_axis],
            y=df_sampled[y_axis],
            mode='markers',
            marker=dict(
                size=4,        # smaller marker = faster rendering
                opacity=0.5,   # semi-transparent
                color='blue'
            )
        ))

        # Minimal layout for speed
        fig.update_layout(
            title=f"{x_axis} vs {y_axis}",
            template="plotly_white",
            xaxis_title=x_axis,
            yaxis_title=y_axis,
            margin=dict(l=40, r=20, t=40, b=40)
        )

        # Display
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")

        # Correlation on sampled data
        corr = df_sampled[x_axis].corr(df_sampled[y_axis])
        col1, col2, col3 = st.columns(3)
        with col1:  # middle column
            st.info(f"📐 Correlation Coefficient: **{corr:.4f}**")

        col1, col2, col3 = st.columns(3)
        with col1:  # first column
            # PNG download
            plotly_png_download(fig, f"{x_axis}_vs_{y_axis}.png")
            database.save_log(f"Generated scatter plot: {x_axis} vs {y_axis}", "Analyst")
            database.save_log(f"Downloaded Box Plot", "Analyst")



# --- TAB 3: ANOMALIES ---
with tab3:
    st.markdown("#### Box Plot Analysis")
    col_x, col_y = st.columns(2)
    with col_x:
        y_axis = st.selectbox("Y Axis", numeric_cols, index=0, key="box_y_axis")
    with col_y:
        group_col = st.selectbox("Group By", ["None"] + categorical_cols, index=0, key="box_group_col")

    if st.button("📦 Generate Box Plot", key="boxplot_btn"):
        df_sampled = sample_df(df)
        fig = px.box(df_sampled, y=y_axis, x=None if group_col == "None" else group_col, points="outliers",
                     title=f"Box Plot of {y_axis}" if group_col == "None" else f"Box Plot of {y_axis} by {group_col}")
        st.plotly_chart(fig, use_container_width=True)
        q1 = df[y_axis].quantile(0.25)
        q3 = df[y_axis].quantile(0.75)
        iqr = q3 - q1
        outlier_count = df[(df[y_axis] < q1 - 1.5*iqr) | (df[y_axis] > q3 + 1.5*iqr)].shape[0]
        
        col1, col2, col3 = st.columns(3)
        with col1:  # middle column
            st.info(f"🚨 Outliers detected: **{outlier_count}**")

        col1, col2, col3 = st.columns(3)
        with col1:  # middle column
            plotly_png_download(fig, f"{x_axis}_vs_{y_axis}.png")
        database.save_log(f"Generated box plot for {y_axis}", "Analyst")
        database.save_log(f"Downloaded Box Plot", "Analyst")


# --- TAB 4: DATA PROFILING ---
with tab4:
    st.markdown("#### Full Dataset Scan")
    if st.button("📑 Generate Profile Report"):
        st.dataframe(df.describe().T, use_container_width=True)
        if df.isnull().sum().sum() > 0:
            st.bar_chart(df.isnull().sum())
        else:
            st.success("No missing data found!")
        database.save_log("Generated full data profile report", "Analyst")

# --- CORRELATION MATRIX ---
st.divider()
st.markdown("### 🔢 Correlation Heatmap")
if len(numeric_cols) > 1:
    corr_matrix = compute_corr_matrix(df, numeric_cols)
    fig_corr = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='RdBu_r', title="Feature Correlation")
    st.plotly_chart(fig_corr, use_container_width=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col3:  # middle column
        plotly_png_download(fig_corr, f"correlation_matrix.png")
        database.save_log(f"Downloaded Correlation Heatmap", "Analyst")
else:
    st.warning("Not enough numeric columns for correlation.")