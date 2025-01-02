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

# --- Google Sheet CSV URL for Player Stats ---
sheet_url = "https://docs.google.com/spreadsheets/d/1aox-kLc-IBX87_PQUN_E_mrWWzte8iwJMEDdQIFqYXk/export?format=csv"

# --- Fetch Data from Google Sheets ---
df = fetch_data(sheet_url)

# --- App Layout ---
st.title("aFc Richman Stats")
st.caption("Explore and analyze player stats dynamically.")

# --- Add Player Carousel ---
if not df.empty:
    st.markdown("<h2 style='text-align: center;'>Players</h2>", unsafe_allow_html=True)
    
    # Check for required columns (e.g., Player, Position)
    if "Player" in df.columns and "Position" in df.columns:
        # Limit the number of players displayed to 3 (you can adjust this)
        displayed_players = df.head(3)

        carousel_col1, carousel_col2, carousel_col3 = st.columns(3)
        columns = [carousel_col1, carousel_col2, carousel_col3]
        
        for i, player_row in enumerate(displayed_players.itertuples()):
            with columns[i % 3]:
                st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <h3>{player_row.Player}</h3>
                        <p><strong>Position:</strong> {player_row.Position}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.warning("Player data is missing the required 'Player' or 'Position' columns.")
else:
    st.warning("No player data available.")

# --- Add Games Section ---
st.markdown("<h2 style='text-align: center;'>Games</h2>", unsafe_allow_html=True)

# Example placeholder for games (you can fetch game data dynamically if available)
games_results = [
    {"competition": "Eredivisie", "date": "Sun. 22 December 2024", "result": "Sparta 0 - 2 aFc Richman"},
    {"competition": "Dutch Cup", "date": "Thu. 19 December 2024", "result": "aFc Richman 2 - 0 Telstar"},
    {"competition": "Eredivisie", "date": "Sun. 15 December 2024", "result": "aFc Richman 3 - 0 Almere City FC"},
]

for game in games_results:
    st.markdown(f"""
        <div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px;">
            <strong>{game['competition']}</strong><br>
            <span>{game['date']}</span><br>
            <span style="font-size: 18px;">{game['result']}</span>
        </div>
    """, unsafe_allow_html=True)

# --- Tabs for Navigation ---
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Charts", "Club", "Team"])

# Tab 1: Overview
with tab1:
    st.subheader("Player Stats")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No data available.")

# Tab 2: Charts
with tab2:
    st.header("Charts")
    if not df.empty:
        chart_type = st.radio("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot"])
        selected_column = st.selectbox("Select a Column to Plot", df.select_dtypes(include=["number"]).columns)
        if selected_column:
            chart_kwargs = {"data_frame": df, "x": 'Player', "y": selected_column, "title": f"{selected_column} by Player"}
            fig = px.bar(**chart_kwargs) if chart_type == "Bar Chart" else px.line(**chart_kwargs) if chart_type == "Line Chart" else px.scatter(**chart_kwargs)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available.")

# Tab 3: Club
with tab3:
    st.header("Club Information")
    st.markdown("Detailed stats and league matches for the club.")

# Tab 4: Team
with tab4:
    st.header("Team Information")
    if not df.empty:
        st.dataframe(df)
    else:
        st.warning("No team data available.")
