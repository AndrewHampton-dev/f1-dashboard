import streamlit as st
import fastf1 as ff1
import pandas as pd
import sys
#sys.path.insert(0, "../app")
from app.data_loader import *




st.set_page_config(page_title="F1 Head-to-Head", layout="wide")
st.title("🏎️ F1 Head-to-Head Comparison")


seasons = get_available_seasons()

selected_season = st.sidebar.selectbox(
    "Select Season",
    options=seasons,
    index=len(seasons) - 1  # Default to most recent
)

with st.spinner(f"Loading data for {selected_season}..."):
        team_drivers = get_season_teams_and_drivers(selected_season)


if not team_drivers:
    st.error(f"No data available for {selected_season}. Try a different season.")
    st.stop()

available_teams = sorted(list(team_drivers.keys()))
selected_team = st.sidebar.selectbox(
    "Select Team",
    options=available_teams
)

drivers_for_team = team_drivers[selected_team]
if len(drivers_for_team) < 2:
    st.warning(f"Only {len(drivers_for_team)} driver(s) found for {selected_team} in {selected_season}. Need at least 2 for comparison.")
    st.stop()



# Get full names for display
driver_full_names = {}
for code in drivers_for_team:
    name = get_driver_full_name(code, selected_season)
    driver_full_names[code] = f"{code} - {name}"


col1, col2 = st.columns(2)
with col1:
    driver1_code = st.sidebar.selectbox(
        "Driver 1",
        options=drivers_for_team,
        format_func=lambda x: driver_full_names.get(x, x),
        index=0
    )
with col2:
    # Exclude Driver 1 from Driver 2 options
    driver2_options = [d for d in drivers_for_team if d != driver1_code]
    driver2_code = st.sidebar.selectbox(
        "Driver 2",
        options=driver2_options,
        format_func=lambda x: driver_full_names.get(x, x),
        index=0
    )

if st.sidebar.button("Compare Drivers", type="primary"):
    with st.spinner("Calculating stats..."):
        stats1 = get_driver_stats(selected_season, driver1_code)
        stats2 = get_driver_stats(selected_season, driver2_code)
    
    # Display comparison
    st.divider()
    st.subheader(f"📊 {selected_season} Season Comparison")
    st.caption(f"Team: {selected_team}")
    
    # Side-by-side metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 🏎️ {driver1_code}")
        st.metric("Team", stats1["Team"])
        st.metric("Races", stats1["Races"])
        st.metric("Points", stats1["Points"])
        st.metric("Wins", stats1["Wins"])
        st.metric("Poles", stats1["Poles"])
        st.metric("DNFs", stats1["DNFs"])
        if stats1["Avg_Grid"]:
            st.metric("Avg Grid Position", f"{stats1['Avg_Grid']:.1f}")
        if stats1["Avg_Finish"]:
            st.metric("Avg Finish Position", f"{stats1['Avg_Finish']:.1f}")
    
    with col2:
        st.markdown(f"### 🏎️ {driver2_code}")
        st.metric("Team", stats2["Team"])
        st.metric("Races", stats2["Races"])
        st.metric("Points", stats2["Points"])
        st.metric("Wins", stats2["Wins"])
        st.metric("Poles", stats2["Poles"])
        st.metric("DNFs", stats2["DNFs"])
        if stats2["Avg_Grid"]:
            st.metric("Avg Grid Position", f"{stats2['Avg_Grid']:.1f}")
        if stats2["Avg_Finish"]:
            st.metric("Avg Finish Position", f"{stats2['Avg_Finish']:.1f}")