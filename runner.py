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
sheet_url = "https://docs.google.com/spreadsheets/d/1aox-kLc-IBX87_PQUN_E_mrWWzte8iwJMEDdQIFqYXk/export?format=csv"

# --- Google Sheet CSV URL for Team Data ---
team_sheet_url = "https://docs.google.com/spreadsheets/d/1aox-kLc-IBX87_PQUN_E_mrWWzte8iwJMEDdQIFqYXk/export?format=csv&gid=1002186620"

# Fetch data from the Google Sheets
df = fetch_data(sheet_url)
df_teams = fetch_data(team_sheet_url)

# --- Helper Function to Convert Data to CSV ---
def convert_df_to_csv(data):
    return data.to_csv(index=False).encode('utf-8')

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
            <h1 style="font-size:40px; font-weight:bold; color:#2c3e50; text-align:center;">
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
        st.header("Club Information")
        
        # Add Club Description
        st.markdown(
            """
            Explore detailed stats and league matches for the club.
            Use the link below to view the Club League Matches on Pro Clubs Head:
            """
        )

        # Add Clickable Link
        st.markdown("[View Club League Matches](https://proclubshead.com/25/club-league-matches/gen5-353675/)")

        # Embed the Website (Enhanced Style)
        st.markdown(
            """
            <style>
                iframe {
                    border: none;
                    overflow: hidden;
                    background-color: transparent;
                    width: 100%;
                    height: 800px;
                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5); /* Adds shadow for better integration */
                }
            </style>
            <iframe src="https://proclubshead.com/25/club-league-matches/gen5-353675/" 
            width="100%" height="800" frameborder="0"></iframe>
            """,
            unsafe_allow_html=True
        )
    
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
        st.success("Data refreshed successfully!")
