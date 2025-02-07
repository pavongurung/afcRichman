import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Configurations ---
st.set_page_config(
    page_title="AFC Richman",
    layout="wide"
)

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
        body {
            font-family: 'Koulen', sans-serif;
            background-color: #000000;
            color: #ffffff;
        }
        h1 {
            font-size: 50px;
            font-weight: bold;
            color: #e74c3c;
            text-align: center;
            margin-bottom: 5px;
        }
        h2 {
            font-size: 30px;
            font-weight: bold;
            color: #ffffff;
            text-align: center;
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
        /* Center text in tables */
        table {
            text-align: center;
            font-size: 18px;
        }
        th, td {
            text-align: center !important;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Koulen&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# --- BIG HEADER FOR AFC RICHMAN ---
st.markdown("<h1>AFC RICHMAN</h1>", unsafe_allow_html=True)

# --- Navigation Tabs for Sections ---
tab1, tab2, tab3 = st.tabs(["Player Stats", "Standings", "Fixtures"])

# --- QFG STATS TAB ---
with tab1:
    st.subheader("Player Stats")

    # --- Fetch Data from Google Sheet ---
    @st.cache_data
    def fetch_data(sheet_url: str):
        try:
            df = pd.read_csv(sheet_url)
            if df.empty:
                st.warning("The fetched data is empty.")
            df.dropna(how="all", inplace=True)  # Remove empty rows
            return df
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return pd.DataFrame()

    # --- Google Sheet CSV URL for Player Stats ---
    sheet_url = "https://docs.google.com/spreadsheets/d/1LayywggB9GCx1HwluNxc88_jLrjFU7jo5FNA7YbY8ME/export?format=csv&gid=421420318"
    df = fetch_data(sheet_url)

    if not df.empty:
        # Remove Index
        df.reset_index(drop=True, inplace=True)

        # Clean Numeric Columns (Handle NaN Errors)
        numeric_cols = df.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, set invalid values to NaN
            df[col].fillna(0, inplace=True)  # Replace NaN with 0

        # Display DataFrame with Center Alignment
        st.dataframe(df.style.set_properties(**{"text-align": "center"}), use_container_width=True, height=600)

        # Leaderboard Section
        st.subheader("Top Performers")
        stat_category = st.selectbox("Select Stat Category", numeric_cols)
        if stat_category:
            leaderboard = df.nlargest(3, stat_category)[["Player", stat_category]]
            st.write(f"Top 3 Players for {stat_category}:")
            st.dataframe(leaderboard.style.hide_index().set_properties(**{"text-align": "center"}))

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

# --- FIXTURES TAB ---
with tab3:
    st.title("Fixtures")

    # --- Fixture Data ---
    fixtures = [
        ("February 3, 2025", "Trakas HDSPM", "9:00 PM"),
        ("February 3, 2025", "Titans Inferno", "9:30 PM"),
        ("February 6, 2025", "RTG Academy", "8:30 PM"),
        ("February 6, 2025", "Reggae Boyzzz", "9:00 PM"),
        ("February 10, 2025", "Real Smokey", "9:00 PM"),
        ("February 10, 2025", "Purple Hollow", "9:30 PM"),
        ("March 3, 2025", "FC Wockhardt", "9:00 PM"),
        ("March 3, 2025", "FC Dragonfire", "9:30 PM"),
        ("March 6, 2025", "East Clan", "8:30 PM"),
        ("March 6, 2025", "Trakas HDSPM", "9:00 PM"),
        ("March 17, 2025", "Titans Inferno", "9:00 PM"),
        ("March 17, 2025", "RTG Academy", "9:30 PM"),
        ("March 31, 2025", "NB Rovers", "9:30 PM"),
        ("April 3, 2025", "Out of Shape FC", "8:30 PM"),
        ("April 3, 2025", "Kings TM", "9:00 PM"),
        ("April 7, 2025", "Raptors FC", "9:00 PM"),
        ("April 7, 2025", "Jogo Bonito", "9:30 PM"),
        ("April 10, 2025", "Girth City", "8:30 PM"),
        ("April 10, 2025", "FC Wockhardt", "9:00 PM"),
        ("April 14, 2025", "FC Dragonfire", "9:00 PM"),
        ("April 14, 2025", "East Clan", "9:30 PM"),
    ]

    # Convert to DataFrame and Filter
    df_fixtures = pd.DataFrame(fixtures, columns=["Date", "Opponent", "Time"])
    df_fixtures["DateTime"] = pd.to_datetime(df_fixtures["Date"] + " " + df_fixtures["Time"])
    upcoming_fixtures = df_fixtures[df_fixtures["DateTime"] >= datetime.now()]
    
    st.subheader("Upcoming Fixtures")
    st.table(upcoming_fixtures[["Date", "Opponent", "Time"]].style.hide_index().set_properties(**{"text-align": "center"}))
