import streamlit as st
import pandas as pd
import datetime
import time

# --- Page Configurations ---
st.set_page_config(
    page_title="AFC Richman - QFG Stats",
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
        /* Countdown Styling */
        .countdown-box {
            display: flex;
            justify-content: center;
            gap: 15px;
            font-size: 35px;
            font-weight: bold;
            margin-top: 10px;
        }
        .countdown-item {
            color: #e74c3c;
            background: #222;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            width: 80px;
        }
        /* Fixtures Styling */
        .fixtures-box {
            font-size: 18px;
            color: #ffffff;
            text-align: center;
        }
        .fixtures-box strong {
            color: #e74c3c;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Koulen&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# --- BIG HEADER FOR AFC RICHMAN ---
st.markdown("<h1>AFC RICHMAN</h1>", unsafe_allow_html=True)
st.markdown("<h2>QFG STATS</h2>", unsafe_allow_html=True)

# --- Navigation Tabs for Sections ---
tab1, tab2, tab3 = st.tabs(["QFG Stats", "Standings", "Fixtures"])

# --- QFG STATS TAB ---
with tab1:
    st.subheader("Player Stats")
    
    # --- Function to Fetch Data from Google Sheet ---
    @st.cache_data
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

    if not df.empty:
        # Convert numeric columns
        numeric_cols = df.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric
            df[col].fillna(0, inplace=True)  # Replace NaN with 0

        # Display DataFrame
        st.dataframe(df, use_container_width=True, height=600)

        # Leaderboard Section
        st.subheader("Top Performers")
        stat_category = st.selectbox("Select Stat Category", numeric_cols)
        if stat_category:
            leaderboard = df.nlargest(3, stat_category)[["Player", stat_category]]
            st.write(f"Top 3 Players for {stat_category}:")
            st.dataframe(leaderboard)

        # Player Comparison Section
        st.subheader("Compare Players")
        players = st.multiselect("Select Two Players to Compare", df["Player"].unique(), max_selections=2)
        if len(players) == 2:
            comparison = df[df["Player"].isin(players)].set_index("Player")
            st.write(f"Comparison of {players[0]} vs {players[1]}:")
            st.dataframe(comparison[numeric_cols])

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
    st.title("Upcoming Fixtures")

    # --- Fixture List ---
    fixtures = [
        ("February 3", "Trakas HDSPM", "9:00 EST"),
        ("February 6", "RTG Academy", "8:30 EST"),
        ("February 10", "Real Smokey", "9:00 EST"),
        ("March 3", "FC Wockhardt", "9:00 EST"),
        ("March 6", "East Clan", "8:30 EST"),
        ("March 17", "Titans Inferno", "9:00 EST"),
        ("March 31", "NB Rovers", "9:30 EST"),
        ("April 3", "Out of Shape FC", "8:30 EST"),
        ("April 7", "Raptors FC", "9:00 EST"),
        ("April 10", "Girth City", "8:30 EST"),
        ("April 14", "FC Dragonfire", "9:00 EST"),
    ]

    # --- Find Next Match ---
    current_time = datetime.datetime.now()
    next_match = None

    for match_date, opponent, time_str in fixtures:
        match_datetime = datetime.datetime.strptime(f"{match_date} {time_str}", "%B %d %I:%M %p EST")
        if match_datetime > current_time:
            next_match = (match_date, opponent, match_datetime)
            break

    if next_match:
        st.subheader(f"Next Match: {next_match[1]} on {next_match[0]} at {time_str}")
        
        # --- Countdown Timer ---
        time_remaining = next_match[2] - current_time
        days, seconds = divmod(time_remaining.total_seconds(), 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        
        st.markdown(f"""
        <div class="countdown-box">
            <div class="countdown-item">{int(days)}<br><span style="font-size: 18px;">DAYS</span></div>
            <div class="countdown-item">{int(hours)}<br><span style="font-size: 18px;">HOURS</span></div>
            <div class="countdown-item">{int(minutes)}<br><span style="font-size: 18px;">MINS</span></div>
            <div class="countdown-item">{int(seconds)}<br><span style="font-size: 18px;">SECS</span></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.subheader("No upcoming matches scheduled.")

