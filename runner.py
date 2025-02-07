import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configurations ---
st.set_page_config(
    page_title="QFG Stats",
    layout="wide"
)

# --- Function to Fetch Data from Google Sheet ---
def fetch_data(sheet_url: str):
    try:
        df = pd.read_csv(sheet_url)
        if df.empty:
            st.warning("The fetched data is empty.")
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# --- Google Sheet CSV URL for QFG Stats ---
sheet_url = "https://docs.google.com/spreadsheets/d/1LayywggB9GCx1HwluNxc88_jLrjFU7jo5FNA7YbY8ME/export?format=csv&gid=421420318"

# Fetch data
df = fetch_data(sheet_url)

# --- Custom CSS for Red, Black, and Koulen Font ---
st.markdown("""
    <style>
        body {
            font-family: 'Koulen', sans-serif;
            background-color: #000000;
            color: #ffffff;
        }
        h1 {
            font-size: 40px;
            font-weight: bold;
            color: #e74c3c;
            text-align: center; 
        }
        .stat {
            font-size: 22px;
            font-weight: bold;
            color: #ffffff;
        }
        .stButton button {
            background-color: #e74c3c;
            color: white;
            font-size: 16px;
            border: none;
        }
        .stButton button:hover {
            background-color: #c0392b;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Koulen&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# --- App Layout ---
st.title("QFG STATS")

# Check if data is loaded successfully
if not df.empty:
    # Clean Numeric Columns (Handle NaN Errors)
    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, set invalid values to NaN
        df[col].fillna(0, inplace=True)  # Replace NaN with 0

    # Display DataFrame without index
    st.subheader("Player Stats")
    st.dataframe(df.reset_index(drop=True), use_container_width=True, height=600, hide_index=True)

    # Leaderboard Section
    st.subheader("Top Performers")
    stat_category = st.selectbox("Select Stat Category", numeric_cols)
    if stat_category:
        leaderboard = df.nlargest(3, stat_category)[["Player", stat_category]]
        st.write(f"Top 3 Players for {stat_category}:")
        st.dataframe(leaderboard, hide_index=True)

    # Player Comparison Section
    st.subheader("Compare Players")
    players = st.multiselect("Select Two Players to Compare", df["Player"].unique(), max_selections=2)
    if len(players) == 2:
        comparison = df[df["Player"].isin(players)].set_index("Player")
        st.write(f"Comparison of {players[0]} vs {players[1]}:")
        st.dataframe(comparison[numeric_cols], hide_index=False)
    elif len(players) > 2:
        st.warning("Please select only two players.")

# --- Manual Refresh Button ---
if st.button("Refresh Data"):
    with st.spinner('Refreshing data...'):
        df = fetch_data(sheet_url)
        st.success("Data refreshed successfully!")
