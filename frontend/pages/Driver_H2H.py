import streamlit as st
import fastf1 as ff1
import pandas as pd
from datetime import datetime
import sys
sys.path.insert(0, "../app")
from app import data_loader

@st.cache_data
def get_season_teams_and_drivers(season):
    """
    Returns a dictionary: {team_name: [list of driver codes who raced for that team]}
    """
    # Get the season schedule
    schedule = ff1.get_event_schedule(season, include_testing=False)

    # Store all drivers per team
    team_drivers = {}
    
    for _, event in schedule.iterrows():
        event_name = event["EventName"]
        
        # Load the race session (lightweight, no telemetry)
        try:
            race = ff1.get_session(season, event_name, "R")
            race.load(laps=False, telemetry=False, weather=False, messages=False)
            
            # Get unique driver-team combinations for this race
            for _, row in race.results.iterrows():
                driver = row["Abbreviation"]
                team = row["TeamName"]
                
                # Add driver to this team's set
                if team not in team_drivers:
                    team_drivers[team] = set()
                team_drivers[team].add(driver)
                
        except Exception as e:
            # Skip races that fail to load
            continue
    
    # Convert sets to sorted lists
    return {team: sorted(list(drivers)) for team, drivers in team_drivers.items()}

@st.cache_data
def get_driver_full_name(driver_code, season):
    """Get the full name of a driver from their code"""
    # FastF1 doesn't have a direct lookup, so we need to load a session
    schedule = ff1.get_event_schedule(season, include_testing=False)
    if schedule.empty:
        return driver_code
    
    # Try the first race of the season
    try:
        race = ff1.get_session(season, schedule.iloc[0]["EventName"], "R")
        race.load(laps=False, telemetry=False, weather=False, messages=False)
        
        driver_row = race.results[race.results["Abbreviation"] == driver_code]
        if not driver_row.empty:
            return driver_row.iloc[0]["FullName"]
    except:
        pass
    
    return driver_code  # Fallback to code if name not found

def get_available_seasons():
    """Get all seasons from 1950 to current year"""
    current_year = datetime.now().year
    return list(range(1950, current_year + 1))

def get_driver_stats(season, driver_code):
    """Get aggregate stats for a driver across a season"""
    schedule = ff1.get_event_schedule(season, include_testing=False)
    
    stats = {
        "Races": 0,
        "Points": 0,
        "Wins": 0,
        "Poles": 0,
        "DNFs": 0,
        "Team": None,
        "Avg_Grid": [],
        "Avg_Finish": [],
    }
    
    for _, event in schedule.iterrows():
        event_name = event["EventName"]
        
        try:
            # Load race
            race = ff1.get_session(season, event_name, "R")
            race.load(laps=False, telemetry=False, weather=False, messages=False)
            
            driver_row = race.results[race.results["Abbreviation"] == driver_code]
            if driver_row.empty:
                continue  # Driver didn't participate
                
            driver_row = driver_row.iloc[0]
            stats["Races"] += 1
            stats["Team"] = driver_row["TeamName"]  # Last team they raced for
            
            # Points
            stats["Points"] += driver_row["Points"]
            
            # Win
            if driver_row["Position"] == 1:
                stats["Wins"] += 1
            
            # DNF check
            position = driver_row["Position"]
            status = driver_row.get("Status", "")
            is_dnf = (
                position == "DNF" or 
                position == "DNS" or 
                status not in ["Finished", "Classified"] or
                pd.isna(position)
            )
            if is_dnf:
                stats["DNFs"] += 1
            
            # Average grid position
            try:
                quali = ff1.get_session(season, event_name, "Q")
                quali.load(laps=False, telemetry=False, weather=False, messages=False)
                quali_row = quali.results[quali.results["Abbreviation"] == driver_code]
                if not quali_row.empty:
                    stats["Avg_Grid"].append(float(quali_row.iloc[0]["Position"]))
            except:
                pass  # No qualifying data
            
            # Average finish position (only finished races)
            if not is_dnf:
                stats["Avg_Finish"].append(float(position))
                
        except Exception as e:
            continue  # Skip sessions that fail
    
    # Calculate averages
    stats["Avg_Grid"] = sum(stats["Avg_Grid"]) / len(stats["Avg_Grid"]) if stats["Avg_Grid"] else None
    stats["Avg_Finish"] = sum(stats["Avg_Finish"]) / len(stats["Avg_Finish"]) if stats["Avg_Finish"] else None
    
    return stats


st.set_page_config(page_title="F1 Head-to-Head", layout="wide")
st.title("🏎️ F1 Head-to-Head Comparison")

# 1. Season Selector
seasons = get_available_seasons()
selected_season = st.selectbox(
    "Select Season",
    options=seasons,
    index=len(seasons) - 1  # Default to most recent
)

# 2. Get teams and drivers for the selected season
with st.spinner(f"Loading data for {selected_season}..."):
    team_drivers = get_season_teams_and_drivers(selected_season)

if not team_drivers:
    st.error(f"No data available for {selected_season}. Try a different season.")
    st.stop()

# 3. Team Selector
available_teams = sorted(list(team_drivers.keys()))
selected_team = st.selectbox(
    "Select Team",
    options=available_teams
)

# 4. Driver Selectors (two drivers from the same team)
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
    driver1_code = st.selectbox(
        "Driver 1",
        options=drivers_for_team,
        format_func=lambda x: driver_full_names.get(x, x),
        index=0
    )
with col2:
    # Exclude Driver 1 from Driver 2 options
    driver2_options = [d for d in drivers_for_team if d != driver1_code]
    driver2_code = st.selectbox(
        "Driver 2",
        options=driver2_options,
        format_func=lambda x: driver_full_names.get(x, x),
        index=0
    )

# 5. Compare button
if st.button("Compare Drivers", type="primary"):
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