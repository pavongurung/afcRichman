import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- Page Configurations ---
st.set_page_config(
    page_title="aFc Richman Stats",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stApp {
        max-width: 100%;
    }
    .stat-card {
        background-color: #1E1E1E;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem;
    }
    .metric-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #FFFFFF;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #4CAF50;
    }
    div[data-testid="stSidebarNav"] li div a {
        margin-left: 1rem;
        padding: 1rem;
        width: 300px;
        border-radius: 0.5rem;
        background-color: #262730;
    }
    /* Custom styling for dataframes */
    .dataframe {
        font-family: 'Arial', sans-serif;
        border-collapse: collapse;
        width: 100%;
    }
    .dataframe th {
        background-color: #2C3E50;
        color: white;
        padding: 12px;
        text-align: left;
    }
    .dataframe td {
        padding: 8px;
        border-bottom: 1px solid #ddd;
    }
    .dataframe tr:hover {
        background-color: #1E1E1E;
    }
    </style>
""", unsafe_allow_html=True)

# --- Function to Fetch Data from Google Sheet ---
@st.cache_data(ttl=300)  # Cache data for 5 minutes
def fetch_data(sheet_url: str):
    try:
        return pd.read_csv(sheet_url)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# --- URLs and Data Fetching ---
sheet_url = "https://docs.google.com/spreadsheets/d/1aox-kLc-IBX87_PQUN_E_mrWWzte8iwJMEDdQIFqYXk/export?format=csv"
team_sheet_url = "https://docs.google.com/spreadsheets/d/1aox-kLc-IBX87_PQUN_E_mrWWzte8iwJMEDdQIFqYXk/export?format=csv&gid=1002186620"

df = fetch_data(sheet_url)
df_teams = fetch_data(team_sheet_url)

# --- App Header ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("⚽ aFc Richman Stats")
    st.caption("Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

st.markdown("""
    <div style='background-color: #2C3E50; padding: 1rem; border-radius: 0.5rem; text-align: center; margin: 1rem 0;'>
        <h3 style='color: white; margin: 0;'>
            Appearances, goals, and assists are tracked only for 11v11 friendlies and competitive matches
        </h3>
    </div>
""", unsafe_allow_html=True)

if not df.empty:
    # Clean Numeric Columns
    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # --- Key Metrics Dashboard ---
    st.markdown("### 📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class='stat-card'>
                <p class='metric-title'>Total Goals</p>
                <p class='metric-value'>{}</p>
            </div>
        """.format(int(df['Goals'].sum())), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='stat-card'>
                <p class='metric-title'>Total Assists</p>
                <p class='metric-value'>{}</p>
            </div>
        """.format(int(df['Assists'].sum())), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='stat-card'>
                <p class='metric-title'>Clean Sheets</p>
                <p class='metric-value'>{}</p>
            </div>
        """.format(int(df['Clean Sheets'].sum())), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class='stat-card'>
                <p class='metric-title'>Total Players</p>
                <p class='metric-value'>{}</p>
            </div>
        """.format(len(df)), unsafe_allow_html=True)

    # --- Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "📊 Charts", "🏆 Club", "👥 Team"])

    with tab1:
        # Player Stats Table
        st.markdown("### Player Statistics")
        st.dataframe(
            df.style.background_gradient(subset=numeric_cols, cmap='YlOrRd'),
            use_container_width=True,
            height=400,
            hide_index=True
        )

        # Top Performers
        st.markdown("### 🏅 Top Performers")
        stat_category = st.selectbox("Select Stat Category", numeric_cols)
        if stat_category:
            leaderboard = df.nlargest(3, stat_category)[["Player", stat_category]]
            
            # Create a more visually appealing leaderboard
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=leaderboard["Player"],
                y=leaderboard[stat_category],
                text=leaderboard[stat_category],
                textposition='auto',
                marker_color=['gold', 'silver', '#CD7F32']
            ))
            fig.update_layout(
                title=f"Top 3 Players - {stat_category}",
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

        # Player Comparison
        st.markdown("### 🔄 Player Comparison")
        col1, col2 = st.columns(2)
        with col1:
            player1 = st.selectbox("Select First Player", df["Player"].unique(), key="player1")
        with col2:
            player2 = st.selectbox("Select Second Player", df["Player"].unique(), key="player2")
        
        if player1 and player2 and player1 != player2:
            comparison = df[df["Player"].isin([player1, player2])].set_index("Player")[numeric_cols]
            
            # Create radar chart for comparison
            categories = numeric_cols
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=comparison.loc[player1],
                theta=categories,
                fill='toself',
                name=player1
            ))
            fig.add_trace(go.Scatterpolar(
                r=comparison.loc[player2],
                theta=categories,
                fill='toself',
                name=player2
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max(comparison.max().max(), 1)]
                    )),
                showlegend=True,
                title="Player Comparison Radar Chart",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### 📈 Performance Charts")
        
        # Enhanced Chart Options
        chart_type = st.radio(
            "Select Visualization Type",
            ["Bar Chart", "Line Chart", "Scatter Plot", "Heat Map"],
            horizontal=True
        )
        
        selected_column = st.selectbox("Select Metric to Visualize", numeric_cols)
        
        if not df.empty:
            if chart_type == "Heat Map":
                fig = px.imshow(
                    df[numeric_cols].corr(),
                    labels=dict(color="Correlation"),
                    title="Metrics Correlation Heatmap"
                )
            else:
                chart_kwargs = {
                    "data_frame": df,
                    "x": 'Player',
                    "y": selected_column,
                    "title": f"{selected_column} by Player",
                    "labels": {"Player": "Player Name", selected_column: "Value"},
                    "height": 500,
                    "color_discrete_sequence": px.colors.qualitative.Set3
                }
                
                if chart_type == "Bar Chart":
                    fig = px.bar(**chart_kwargs)
                elif chart_type == "Line Chart":
                    fig = px.line(**chart_kwargs)
                else:
                    fig = px.scatter(**chart_kwargs)
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_title="Player",
                    yaxis_title=selected_column
                )
            
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("### 🏆 Club Information")
        
        # Club Stats Summary
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div style='background-color
            """)
