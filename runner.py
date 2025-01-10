import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- Page Configurations ---
st.set_page_config(
    page_title="aFc Richman Stats",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stApp {
        max-width: 100%;
    }
    .stat-card {
        background-color: #1E1E1E;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem;
    }
    .metric-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #FFFFFF;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #4CAF50;
    }
    div[data-testid="stSidebarNav"] li div a {
        margin-left: 1rem;
        padding: 1rem;
        width: 300px;
        border-radius: 0.5rem;
        background-color: #262730;
    }
    /* Custom styling for dataframes */
    .dataframe {
        font-family: 'Arial', sans-serif;
        border-collapse: collapse;
        width: 100%;
    }
    .dataframe th {
        background-color: #2C3E50;
        color: white;
        padding: 12px;
        text-align: left;
    }
    .dataframe td {
        padding: 8px;
        border-bottom: 1px solid #ddd;
    }
    .dataframe tr:hover {
        background-color: #1E1E1E;
    }
    </style>
""", unsafe_allow_html=True)

# --- Function to Fetch Data from Google Sheets ---
@st.cache_data(ttl=300)  # Cache data for 5 minutes
def fetch_data(sheet_url: str):
    try:
        return pd.read_csv(sheet_url)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# --- URLs and Data Fetching ---
sheet_url = "https://docs.google.com/spreadsheets/d/1aox-kLc-IBX87_PQUN_E_mrWWzte8iwJMEDdQIFqYXk/export?format=csv"
team_sheet_url = "https://docs.google.com/spreadsheets/d/1aox-kLc-IBX87_PQUN_E_mrWWzte8iwJMEDdQIFqYXk/export?format=csv&gid=1002186620"

df = fetch_data(sheet_url)
df_teams = fetch_data(team_sheet_url)

# --- App Header ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("⚽ aFc Richman Stats")
    st.caption("Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

st.markdown("""
    <div style='background-color: #2C3E50; padding: 1rem; border-radius: 0.5rem; text-align: center; margin: 1rem 0;'>
        <h3 style='color: white; margin: 0;'>
            Appearances, goals, and assists are tracked only for 11v11 friendlies and competitive matches
        </h3>
    </div>
""", unsafe_allow_html=True)

if not df.empty:
    # Clean Numeric Columns
    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # --- Key Metrics Dashboard ---
    st.markdown("### 📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
