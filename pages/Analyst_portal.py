import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

from src.data_processor import DataProcessor

st.title("🔬 Analyst portal")

#SAFETY CHECK

if "df" not in st.session_state or st.session_state is None:
    st.warning("No Dataset loaded yet.")
    st.stop()

df = st.session_state.df

st.subheader("📊Data Preview")
st.dataframe(df, height=min(600, 30*(df.shape[0])))

#REAL CLEANING

st.subheader("🧹 Data Cleaning")

if st.button("Clean Data"):
    original_rows = df.shape[0]

    # Use DataProcessor to clean the DataFrame
    processor = DataProcessor()
    processor.data = df  # Assign current DataFrame to processor
    cleaned_data = processor.clean_data()  # Cleans rows, columns, duplicates, resets index

    # Update session state
    st.session_state.df = cleaned_data

    # Show success message
    st.success(
        f"Data cleaned! Removed {original_rows - cleaned_data.shape[0]} duplicate/empty rows. "
        f"Now {cleaned_data.shape[0]} rows remain."
    )

df = st.session_state.df #Refresh after cleaning

#REAL DOWNLOAD

st.subheader("💾 Download Cleaned Data")
st.download_button(
    label="Download Cleaned CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name="cleaned_data.csv",
    mime="text/csv")

#CORRELATION MATRIX

st.subheader("📈 Correlation Matrix")

numeric_df = df.select_dtypes(include="number")

if numeric_df.shape[1] < 2:
    st.info("Not enough numeric columns to compute correlation matrix.")
else:
    corr = numeric_df.corr()

    plt.figure(figsize=(10, 6))
    sb.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
    plt.title("Correlation Matrix")

    st.pyplot(plt)
