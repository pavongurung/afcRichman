import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configurations ---
st.set_page_config(
    page_title="aFc Richman Stats",
    layout="wide"
)

# --- Function to Fetch Data from Google Sheet ---
def fetch_data(sheet_url: str):
    try:
        return pd.read_csv(sheet_url)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# --- Updated Google Sheet CSV URL ---
sheet_url = "https://docs.google.com/spreadsheets/d/1aox-kLc-IBX87_PQUN_E_mrWWzte8iwJMEDdQIFqYXk/export?format=csv"

# Fetch data from the Google Sheet
df = fetch_data(sheet_url)

# --- Helper Function to Convert Data to CSV ---
def convert_df_to_csv(data):
    return data.to_csv(index=False).encode('utf-8')

# --- App Layout ---
st.title("aFc Richman Stats")
st.caption("Explore and analyze player stats dynamically.")

# Check if data is loaded successfully
if not df.empty:
    # Clean Numeric Columns (Handle NaN Errors)
    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, set invalid values to NaN
        df[col].fillna(0, inplace=True)  # Replace NaN with 0
    
    # --- Tabs for Navigation ---
    tab1, tab2 = st.tabs(["Overview", "Charts"])

    # Tab 1: Overview
    with tab1:
        # Larger Header for Overview
        st.markdown("""
            <h1 style="font-size:40px; font-weight:bold; color:#2c3e50; text-align:center;">
            Overview
            </h1>
        """, unsafe_allow_html=True)

        # Expanded DataFrame Display
        st.subheader("Player Stats")
        st.dataframe(df, use_container_width=True, height=600)  # Set height to make it prominent

        # Stats Summary
        st.subheader("Interactive Stats Summary")
        cols = st.columns([1, 1, 1])  # Adjust column layout for the metrics
        for i, col in enumerate(numeric_cols):
            cols[i % 3].metric(
                label=f"{col} (Avg)",
                value=f"{df[col].mean():.2f}"
            )

    # Tab 2: Charts
    with tab2:
        st.header("Charts")

        # Dynamic Chart Type Selection
        chart_type = st.radio("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot"])

        # Generate Chart
        st.subheader(f"{chart_type} of Player Stats")
        selected_column = st.selectbox("Select a Column to Plot", numeric_cols)
        if not df.empty:
            chart_kwargs = {
                "data_frame": df,
                "x": 'Player' if 'Player' in df.columns else df.index,
                "y": selected_column,
                "title": f"{selected_column} by Player",
                "labels": {"Player": "Player Name", selected_column: "Value"},
                "height": 600,
            }

            if chart_type == "Bar Chart":
                fig = px.bar(**chart_kwargs)
            elif chart_type == "Line Chart":
                fig = px.line(**chart_kwargs)
            elif chart_type == "Scatter Plot":
                fig = px.scatter(**chart_kwargs)

            st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available. Please check the Google Sheet URL or try again later.")

# --- Manual Refresh Button ---
if st.button("Refresh Data"):
    df = fetch_data(sheet_url)
    st.write("Data refreshed successfully!")
