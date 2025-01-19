import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# --- Page Configurations ---
st.set_page_config(
    page_title="aFc Richman Stats",
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

# --- Function to Fetch Data from EA API ---
def fetch_ea_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from EA API: {e}")
        return None

# --- Google Sheet URLs ---
sheet_url = "https://docs.google.com/spreadsheets/d/1aox-kLc-IBX87_PQUN_E_mrWWzte8iwJMEDdQIFqYXk/export?format=csv"
team_sheet_url = "https://docs.google.com/spreadsheets/d/1aox-kLc-IBX87_PQUN_E_mrWWzte8iwJMEDdQIFqYXk/export?format=csv&gid=1002186620"
friendlies_sheet_url = "https://docs.google.com/spreadsheets/d/1aox-kLc-IBX87_PQUN_E_mrWWzte8iwJMEDdQIFqYXk/export?format=csv&gid=1694477682"
competitive_sheet_url = "https://docs.google.com/spreadsheets/d/1aox-kLc-IBX87_PQUN_E_mrWWzte8iwJMEDdQIFqYXk/export?format=csv&gid=1257709827"

# --- Fetch data from Google Sheets ---
df = fetch_data(sheet_url)
df_teams = fetch_data(team_sheet_url)
df_friendlies = fetch_data(friendlies_sheet_url)
df_competitive = fetch_data(competitive_sheet_url)

# --- EA API URLs ---
club_id = "353675"
overall_stats_url = f"https://proclubs.ea.com/api/fc/clubs/overallStats?platform=common-gen5&clubIds={club_id}"
last_match_url = f"https://proclubs.ea.com/api/fc/clubs/matches?platform=common-gen5&clubIds={club_id}&matchType=leagueMatch&maxResultCount=1"
member_stats_url = f"https://proclubs.ea.com/api/fc/members/stats?platform=common-gen5&clubId={club_id}"

# --- Fetch data from EA API ---
overall_stats = fetch_ea_data(overall_stats_url)
last_match_data = fetch_ea_data(last_match_url)
member_stats = fetch_ea_data(member_stats_url)

# --- Custom CSS for Red, Black, and Koulen Font ---
st.markdown("""
    <style>
        body {
            font-family: 'Koulen', sans-serif;
            background-color: #000000;
            color: #ffffff;
        }
        h1, h2, h3, .stat {
            color: #e74c3c;
        }
        .highlight {
            color: #2ecc71;
        }
        .negative {
            color: #e74c3c;
        }
        .stButton button {
            background-color: #e74c3c;
            color: white;
        }
        .stButton button:hover {
            background-color: #c0392b;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Koulen&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# --- App Layout ---
st.title("aFc Richman Stats")
st.caption("Explore and analyze player stats dynamically.")

# --- Tabs for Navigation ---
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Charts", "Club", "Team"])

# Tab 1: Overview
with tab1:
    st.markdown("<h1 style='text-align: center;'>Overview</h1>", unsafe_allow_html=True)

    if overall_stats:
        st.subheader("Overall Club Stats")
        st.markdown(f"""
            **Wins**: {overall_stats['wins']}  
            **Losses**: {overall_stats['losses']}  
            **Draws**: {overall_stats['draws']}  
            **Goals Scored**: {overall_stats['goalsFor']}  
            **Goals Conceded**: {overall_stats['goalsAgainst']}  
            **Win Percentage**: {overall_stats['winPercentage']}%
        """)

    if last_match_data and "results" in last_match_data:
        st.subheader("Last Match")
        match = last_match_data["results"][0]
        st.markdown(f"""
            **Opponent**: {match['awayTeamName']}  
            **Score**: {match['homeGoals']} - {match['awayGoals']}  
            **Match Date**: {match['matchDate']}
        """)

# Tab 2: Charts
with tab2:
    st.header("Charts")
    chart_type = st.radio("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot"])
    selected_column = st.selectbox("Select a Column to Plot", df.select_dtypes(include=["number"]).columns)
    if not df.empty and selected_column:
        chart_kwargs = {
            "data_frame": df,
            "x": 'Player' if 'Player' in df.columns else df.index,
            "y": selected_column,
            "title": f"{selected_column} by Player",
            "height": 600,
        }
        if chart_type == "Bar Chart":
            fig = px.bar(**chart_kwargs)
        elif chart_type == "Line Chart":
            fig = px.line(**chart_kwargs)
        elif chart_type == "Scatter Plot":
            fig = px.scatter(**chart_kwargs)
        st.plotly_chart(fig, use_container_width=True)

# Tab 3: Club
with tab3:
    st.header("Club Overview")
    if overall_stats:
        st.markdown(f"""
            <p class="stat">Wins: <span class="highlight">{overall_stats['wins']}</span></p>
            <p class="stat">Losses: <span class="negative">{overall_stats['losses']}</span></p>
            <p class="stat">Draws: <span>{overall_stats['draws']}</span></p>
            <p class="stat">Goals For: <span>{overall_stats['goalsFor']}</span></p>
            <p class="stat">Goals Against: <span>{overall_stats['goalsAgainst']}</span></p>
            <p class="stat">Win Percentage: <span>{overall_stats['winPercentage']}%</span></p>
        """, unsafe_allow_html=True)

# Tab 4: Team
with tab4:
    st.header("Team Information")
    if member_stats:
        st.subheader("Player Stats")
        member_df = pd.DataFrame(member_stats['members'])
        st.dataframe(member_df)

# Manual Refresh Button
if st.button("Refresh Data"):
    with st.spinner('Refreshing data...'):
        df = fetch_data(sheet_url)
        df_teams = fetch_data(team_sheet_url)
        df_friendlies = fetch_data(friendlies_sheet_url)
        df_competitive = fetch_data(competitive_sheet_url)
        overall_stats = fetch_ea_data(overall_stats_url)
        last_match_data = fetch_ea_data(last_match_url)
        member_stats = fetch_ea_data(member_stats_url)
        st.success("Data refreshed successfully!")
