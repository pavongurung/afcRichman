import streamlit as st
import pandas as pd
import datetime
import pytz
import time

# --- Page Configurations ---
st.set_page_config(
    page_title="AFC Richman - Fixtures",
    layout="wide"
)

# --- Set EST Timezone ---
est = pytz.timezone("America/New_York")

# --- Custom CSS for Minimalist Styling ---
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
    </style>
""", unsafe_allow_html=True)

# --- BIG HEADER ---
st.markdown("<h1>AFC RICHMAN</h1>", unsafe_allow_html=True)
st.markdown("<h2>Upcoming Fixtures</h2>", unsafe_allow_html=True)

# --- Fixtures Data ---
fixtures = [
    ("February 10, 2025", "Real Smokey", "9:00 PM"),
    ("February 10, 2025", "Purple Hollow", "9:30 PM"),
    ("March 3, 2025", "FC Wockhardt", "9:00 PM"),
    ("March 3, 2025", "FC Dragonfire", "9:30 PM"),
    ("March 6, 2025", "East Clan", "8:30 PM"),
    ("March 6, 2025", "Trakas HDSPM", "9:00 PM"),
    ("March 17, 2025", "Titans Inferno", "9:00 PM"),
    ("March 17, 2025", "RTG Academy", "9:30 PM"),
]

# --- Find Next 2 Matches ---
next_matches = []
current_time_est = datetime.datetime.now(est)

for match_date, opponent, time_str in fixtures:
    match_datetime = datetime.datetime.strptime(f"{match_date} {time_str}", "%B %d, %Y %I:%M %p")
    match_datetime = est.localize(match_datetime)  # Convert to EST timezone

    if match_datetime > current_time_est:
        next_matches.append((match_date, opponent, match_datetime))
        if len(next_matches) == 2:
            break

# --- Display Next Matches & LIVE Countdown ---
if next_matches:
    for i, (match_date, opponent, match_datetime) in enumerate(next_matches):
        st.subheader(f"Upcoming Match {i+1}: {opponent} on {match_date} at {match_datetime.strftime('%I:%M %p EST')}")
        countdown_placeholder = st.empty()

        while True:
            now = datetime.datetime.now(est)
            time_remaining = match_datetime - now
            days, seconds = divmod(time_remaining.total_seconds(), 86400)
            hours, seconds = divmod(seconds, 3600)
            minutes, seconds = divmod(seconds, 60)

            countdown_html = f"""
            <div class="countdown-box">
                <div class="countdown-item">{int(days)}<br><span style="font-size: 18px;">DAYS</span></div>
                <div class="countdown-item">{int(hours)}<br><span style="font-size: 18px;">HOURS</span></div>
                <div class="countdown-item">{int(minutes)}<br><span style="font-size: 18px;">MINS</span></div>
                <div class="countdown-item">{int(seconds)}<br><span style="font-size: 18px;">SECS</span></div>
            </div>
            """
            countdown_placeholder.markdown(countdown_html, unsafe_allow_html=True)
            time.sleep(1)

else:
    st.subheader("No upcoming matches scheduled.")
