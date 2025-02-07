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
        df = pd.read_csv(sheet_url)
        if df.empty:
            st.warning("The fetched data is empty.")
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# --- Google Sheet CSV URL for Player Stats ---
sheet_url = "https://docs.google.com/spreadsheets/d/1LayywggB9GCx1HwluNxc88_jLrjFU7jo5FNA7YbY8ME/edit?gid=421420318#gid=421420318"

# --- Google Sheet CSV URL for Team Data ---
team_sheet_url = "https://docs.google.com/spreadsheets/d/1aox-kLc-IBX87_PQUN_E_mrWWzte8iwJMEDdQIFqYXk/export?format=csv&gid=1002186620"

# --- Google Sheet CSV URL for Friendlies Data ---
friendlies_sheet_url = "https://docs.google.com/spreadsheets/d/1aox-kLc-IBX87_PQUN_E_mrWWzte8iwJMEDdQIFqYXk/export?format=csv&gid=1694477682"

# --- Google Sheet CSV URL for Competitive Data ---
competitive_sheet_url = "https://docs.google.com/spreadsheets/d/1aox-kLc-IBX87_PQUN_E_mrWWzte8iwJMEDdQIFqYXk/export?format=csv&gid=1257709827"

# Fetch data from the Google Sheets
df = fetch_data(sheet_url)
df_teams = fetch_data(team_sheet_url)
df_friendlies = fetch_data(friendlies_sheet_url)
df_competitive = fetch_data(competitive_sheet_url)

# --- Helper Function to Convert Data to CSV ---
def convert_df_to_csv(data):
    return data.to_csv(index=False).encode('utf-8')

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
        h1 {
            font-size: 40px;
            font-weight: bold;
            color: #e74c3c;
        }
        h2 {
            font-size: 32px;
            font-weight: bold;
            color: #e74c3c;
        }
        h3 {
            font-size: 28px;
            font-weight: bold;
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
            font-size: 16px;
            border: none;
        }
        .stButton button:hover {
            background-color: #c0392b;
        }
        .stat {
            font-size: 20px;
            font-weight: bold;
            color: #34495e;
            margin-bottom: 10px;
        }
        .stat span {
            font-size: 22px;
            font-weight: bold;
        }
        .stMarkdown p {
            color: #ffffff;
            font-size: 18px;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Koulen&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# --- App Layout ---
st.title("aFc Richman Stats")
st.caption("Explore and analyze player stats dynamically.")

# Add the description with emphasis
st.markdown("""
    <h2 style="font-size:24px; font-weight:bold; color:#2c3e50; text-align:center;">
        Appearances, goals, and assists are tracked only for 11v11 friendlies and competitive matches.
    </h2>
""", unsafe_allow_html=True)

# Check if data is loaded successfully
if not df.empty:
    # Clean Numeric Columns (Handle NaN Errors)
    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, set invalid values to NaN
        df[col].fillna(0, inplace=True)  # Replace NaN with 0

    # --- Tabs for Navigation ---
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Charts", "Club", "Team"])

    # Tab 1: Overview
    with tab1:
        # Larger Header for Overview
        st.markdown("""
            <h1 style="font-size:40px; font-weight:bold; color:#e74c3c; text-align:center;">
            Overview
            </h1>
        """, unsafe_allow_html=True)

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

    # Tab 2: Charts
    with tab2:
        st.header("Charts")

        # Dynamic Chart Type Selection
        chart_type = st.radio("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot"])

        # Generate Chart
        st.subheader(f"{chart_type} of Player Stats")
        selected_column = st.selectbox("Select a Column to Plot", numeric_cols)
        if not df.empty:
            chart_kwargs = {
                "data_frame": df,
                "x": 'Player' if 'Player' in df.columns else df.index,
                "y": selected_column,
                "title": f"{selected_column} by Player",
                "labels": {"Player": "Player Name", selected_column: "Value"},
                "height": 600,
            }

            if chart_type == "Bar Chart":
                fig = px.bar(**chart_kwargs)
            elif chart_type == "Line Chart":
                fig = px.line(**chart_kwargs)
            elif chart_type == "Scatter Plot":
                fig = px.scatter(**chart_kwargs)

            st.plotly_chart(fig, use_container_width=True)

    # Tab 3: Club Section
    with tab3:
        st.header("Overall Match Stats for 11v11 Friendlies & Competitive Matches")
        
        try:
            # Ensure that both dataframes are not empty
            if not df_friendlies.empty and not df_competitive.empty:
                # Count the games played in both datasets based on "Played" column (assuming it's present)
                total_played_friendlies = df_friendlies['Played'].sum()
                total_played_competitive = df_competitive['Played'].sum()
                
                # Sum total games played
                total_played = total_played_friendlies + total_played_competitive

                # Sum other stats from both datasets
                total_wins = df_friendlies['Win'].sum() + df_competitive['Win'].sum()
                total_draws = df_friendlies['Draw'].sum() + df_competitive['Draw'].sum()
                total_losses = df_friendlies['Lost'].sum() + df_competitive['Lost'].sum()
                total_gf = df_friendlies['GF'].sum() + df_competitive['GF'].sum()
                total_ga = df_friendlies['GA'].sum() + df_competitive['GA'].sum()
            else:
                # Handle case where one of the datasets is empty
                if df_friendlies.empty:
                    total_played = df_competitive['Played'].sum()
                    total_wins = df_competitive['Win'].sum()
                    total_draws = df_competitive['Draw'].sum()
                    total_losses = df_competitive['Lost'].sum()
                    total_gf = df_competitive['GF'].sum()
                    total_ga = df_competitive['GA'].sum()
                else:
                    total_played = df_friendlies['Played'].sum()
                    total_wins = df_friendlies['Win'].sum()
                    total_draws = df_friendlies['Draw'].sum()
                    total_losses = df_friendlies['Lost'].sum()
                    total_gf = df_friendlies['GF'].sum()
                    total_ga = df_friendlies['GA'].sum()

            # Calculate goal difference and win percentage
            total_gd = total_gf - total_ga
            win_percentage = (total_wins / total_played) * 100 if total_played > 0 else 0

            # Round to whole numbers for display
            total_played = int(total_played)
            total_wins = int(total_wins)
            total_draws = int(total_draws)
            total_losses = int(total_losses)
            total_gf = int(total_gf)
            total_ga = int(total_ga)
            total_gd = int(total_gd)
            win_percentage = round(win_percentage)  # Remove decimal points

            # Display stats with enhanced style
            st.markdown(f'<p class="stat">Total Games Played: <span>{total_played}</span></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="stat">Total Wins: <span class="highlight">{total_wins}</span></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="stat">Total Draws: <span>{total_draws}</span></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="stat">Total Losses: <span class="negative">{total_losses}</span></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="stat">Goals For (GF): <span>{total_gf}</span></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="stat">Goals Against (GA): <span>{total_ga}</span></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="stat">Goal Difference (GD): <span class="{"highlight" if total_gd >= 0 else "negative"}">{total_gd}</span></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="stat">Win Percentage: <span>{win_percentage}%</span></p>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred while calculating the stats: {e}")

    # Tab 4: Team Section
    with tab4:
        st.header("Team Information")
        
        if not df_teams.empty:
            # Show Team Data sorted by Position without index
            df_teams_sorted = df_teams.sort_values(by='Position')
            st.subheader("Players by Position")
            st.dataframe(df_teams_sorted[['Player', 'Position']], use_container_width=True, height=600, hide_index=True)
        else:
            st.warning("No team data available.")
else:
    st.warning("No data available. Please check the Google Sheet URL or try again later.")

# --- Manual Refresh Button ---
if st.button("Refresh Data"):
    with st.spinner('Refreshing data...'):
        df = fetch_data(sheet_url)
        df_teams = fetch_data(team_sheet_url)
        df_friendlies = fetch_data(friendlies_sheet_url)
        df_competitive = fetch_data(competitive_sheet_url)
        st.success("Data refreshed successfully!")
