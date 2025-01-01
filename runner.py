import streamlit as st
import pandas as pd

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

# --- Google Sheet CSV URL ---
sheet_url = "https://docs.google.com/spreadsheets/d/1aox-kLc-IBX87_PQUN_E_mrWWzte8iwJMEDdQIFqYXk/export?format=csv"

# Fetch data from the Google Sheet
df = fetch_data(sheet_url)

# --- Styling ---
st.markdown("""
    <style>
        /* Import Google Font Bebas Neue */
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

        /* Global body styling */
        body {
            font-family: 'Bebas Neue', sans-serif;
            background-color: #FFFFFF;
        }

        /* Header styling */
        h1, h2, h3, h4, h5, h6 {
            color: #D00027;
            font-family: 'Bebas Neue', sans-serif;
            text-transform: uppercase;
        }

        /* Table styling */
        table {
            font-size: 18px;
            color: #000000;
        }
        table th {
            background-color: #FDF667;
            color: #D00027;
            font-weight: bold;
            font-size: 20px;
        }
        table td {
            color: #000000;
            font-size: 18px;
        }

        /* Button styling */
        .stButton>button {
            background-color: #D00027;
            color: #FFFFFF;
            border-radius: 5px;
            padding: 10px 20px;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 18px;
        }

        /* Dropdown styling */
        .stSelectbox div[data-baseweb="select"] {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 18px;
            color: #000000;
        }
    </style>
""", unsafe_allow_html=True)

# --- App Layout ---
st.markdown("""
    <h1 style="text-align:center;">
        aFc Richman Stats
    </h1>
    <h2 style="text-align:center; color:#FDF667; background-color:#D00027; padding:10px;">
        Explore Player Performances and Compare Stats
    </h2>
""", unsafe_allow_html=True)

if not df.empty:
    # Clean Numeric Columns (Handle NaN Errors)
    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, set invalid values to NaN
        df[col].fillna(0, inplace=True)  # Replace NaN with 0

    # --- Tabs for Navigation ---
    tab1, tab2 = st.tabs(["Leaderboard", "Player Comparison"])

    # Tab 1: Leaderboard
    with tab1:
        st.subheader("Top 3 Players for Appearance")
        stat_category = "Appearance"  # Fixed category for simplicity
        leaderboard = df.nlargest(3, stat_category)[["Player", stat_category]]
        st.table(leaderboard.style.format({stat_category: "{:.0f}"}))

    # Tab 2: Player Comparison
    with tab2:
        st.subheader("Compare Players")
        selected_players = st.multiselect("Select Two Players to Compare", df["Player"].unique(), max_selections=2)

        if len(selected_players) == 2:
            comparison_df = df[df["Player"].isin(selected_players)][
                ["Player", "Appearance", "Goals", "Assists", "Clean Sheets"]
            ]
            st.table(comparison_df.style.format(
                {"Appearance": "{:.0f}", "Goals": "{:.0f}", "Assists": "{:.0f}", "Clean Sheets": "{:.0f}"}
            ))

else:
    st.warning("No data available. Please check the Google Sheet URL or try again later.")

# --- Refresh Button ---
if st.button("Refresh Data"):
    df = fetch_data(sheet_url)
    st.write("Data refreshed successfully!")
