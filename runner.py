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
        # Remove empty rows
        df.dropna(how="all", inplace=True)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# --- Google Sheet CSV URL for QFG Stats ---
sheet_url = "https://docs.google.com/spreadsheets/d/1LayywggB9GCx1HwluNxc88_jLrjFU7jo5FNA7YbY8ME/export?format=csv&gid=421420318"

# Fetch data
df = fetch_data(sheet_url)

# --- Custom CSS for Styling ---
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
        .nav-tabs {
            display: flex;
            justify-content: center;
            gap: 20px;
            padding: 20px;
        }
        .nav-tabs button {
            font-size: 18px;
            font-weight: bold;
            color: white;
            background-color: #e74c3c;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
            transition: 0.3s;
        }
        .nav-tabs button:hover {
            background-color: #c0392b;
        }
        /* Center numeric values in table */
        .stDataFrame td {
            text-align: center !important;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Koulen&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# --- Navigation Tabs for Sections ---
tab1, tab2 = st.tabs(["QFG Stats", "Standings"])

# --- QFG STATS TAB ---
with tab1:
    st.title("QFG STATS")
    
    if not df.empty:
        # Clean Numeric Columns (Handle NaN Errors)
        numeric_cols = df.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, set invalid values to NaN
            df[col].fillna(0, inplace=True)  # Replace NaN with 0

        # Center data and display DataFrame
        st.subheader("Player Stats")
        st.dataframe(df.style.set_properties(**{"text-align": "center"}), use_container_width=True, height=600)

        # Leaderboard Section
        st.subheader("Top Performers")
        stat_category = st.selectbox("Select Stat Category", numeric_cols)
        if stat_category:
            leaderboard = df.nlargest(3, stat_category)[["Player", stat_category]]
            st.write(f"Top 3 Players for {stat_category}:")
            st.dataframe(leaderboard.style.set_properties(**{"text-align": "center"}))

        # Player Comparison Section
        st.subheader("Compare Players")
        players = st.multiselect("Select Two Players to Compare", df["Player"].unique(), max_selections=2)
        if len(players) == 2:
            comparison = df[df["Player"].isin(players)].set_index("Player")
            st.write(f"Comparison of {players[0]} vs {players[1]}:")
            st.dataframe(comparison[numeric_cols].style.set_properties(**{"text-align": "center"}))
        elif len(players) > 2:
            st.warning("Please select only two players.")

# --- STANDINGS TAB ---
with tab2:
    st.title("League Standings")

    st.markdown("""
    <p style="text-align: center; font-size: 18px; color: white;">
        Click the button below to view the latest standings.
    </p>
    """, unsafe_allow_html=True)

    # Button to Open Standings in a New Tab
    st.markdown("""
    <div style="text-align: center;">
        <a href="https://questforglory.leaguerepublic.com/standingsForDate/43160383/2/-1/-1.html" target="_blank">
            <button style="
                font-size: 20px;
                font-weight: bold;
                color: white;
                background-color: #e74c3c;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
                transition: 0.3s;
            ">View Standings</button>
        </a>
    </div>
    """, unsafe_allow_html=True)

# --- Manual Refresh Button ---
if st.button("Refresh Data"):
    with st.spinner('Refreshing data...'):
        df = fetch_data(sheet_url)
        st.success("Data refreshed successfully!")
