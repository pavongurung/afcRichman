import streamlit as st
import pandas as pd
import datetime

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

# --- FIXTURES TAB ---
with tab3:
    st.title("Upcoming Fixtures")

    # --- Fixture List ---
    fixtures = [
        ("February 3, 2025", "Trakas HDSPM", "9:00 PM"),
        ("February 6, 2025", "RTG Academy", "8:30 PM"),
        ("February 10, 2025", "Real Smokey", "9:00 PM"),
        ("March 3, 2025", "FC Wockhardt", "9:00 PM"),
        ("March 6, 2025", "East Clan", "8:30 PM"),
        ("March 17, 2025", "Titans Inferno", "9:00 PM"),
        ("March 31, 2025", "NB Rovers", "9:30 PM"),
        ("April 3, 2025", "Out of Shape FC", "8:30 PM"),
        ("April 7, 2025", "Raptors FC", "9:00 PM"),
        ("April 10, 2025", "Girth City", "8:30 PM"),
        ("April 14, 2025", "FC Dragonfire", "9:00 PM"),
    ]

    # --- Find Next Match ---
    current_time = datetime.datetime(2025, 2, 7, 2, 0)  # February 7, 2025, at 2 AM
    next_match = None

    for match_date, opponent, time_str in fixtures:
        match_datetime = datetime.datetime.strptime(f"{match_date} {time_str}", "%B %d, %Y %I:%M %p")
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

