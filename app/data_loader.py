import streamlit as st
import fastf1 as ff1 
import pandas as pd
from datetime import datetime 
import os
from fastf1.ergast import Ergast


os.makedirs('fastf1_cache', exist_ok=True)
ff1.Cache.enable_cache('fastf1_cache')

@st.cache_data
def get_available_seasons():
    """Get all seasons from 1950 to current year"""
    current_year = datetime.now().year
    return list(range(1950, current_year + 1))


@st.cache_data
def get_season_schedule(season):
    """Return the event schedule for a given season."""
    return ff1.get_event_schedule(season, include_testing=False)

@st.cache_data
def load_race_session(season, round_number):
	schedule = ff1.get_event_schedule(season)
	event = schedule[schedule["RoundNumber"] == "round_number"].iloc[0]
	session = ff1.get_session(season, event["EventName"], "R")

	session.load(laps=False, telemetry=False, weather=False, messages=False)


@st.cache_data
def load_quali_session(season, round_number):
    """Load qualifying session for a race"""
    schedule = ff1.get_event_schedule(season)
    event = schedule[schedule["RoundNumber"] == round_number].iloc[0]

    try:
        session = ff1.get_session(season, event["EventName"], "Q")
        session.load(laps=False, telemetry=False, weather=False, messages=False)
        return session
    except:
        return None  # Some races don't have qualifying (e.g., old seasons)


@st.cache_data
def get_driver_lap_time(season, event_name, driver):
    try:
        session = ff1.get_session(season, event_name, "R")
        session.load(laps=True, telemetry=False, weather=False, messages=False)

        laps = session.laps.pick_driver(driver)

        if laps.empty:
            return None

        lap_data =  laps[["LapNumber", "LapTime","Compound", "TyreLife", "TrackStatus"]].copy()
        # Convert times to seconds for easier analysis
        lap_data["LapTimeSeconds"] = lap_data["LapTime"].dt.total_seconds()
    except Exception as e:
        return None

    return lap_data


def format_td(td):
    if pd.isnull(td):
        return "-"

    total_seconds = td.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    if minutes > 0:
        return f"{minutes}:{seconds:06.3f}"
    return f"{seconds:06.3f}"


#Custom Y-axis Formatter function for MM:SS.mmm format
def racing_time_formatter(x, pos):
    #Matplotlib converts pandas timedeltas to floating days internally on the axies
    total_seconds = x * 86400 # Convert the days to total seconds
    minutes = int(total_seconds//60)
    seconds = int(total_seconds % 60)
    milliseconds = int(round((total_seconds % 1) * 1000))
    
    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"



@st.cache_data
def get_teams_and_drivers(seasons: list):
    pass


   # for season in seasons:
  #      schedule = ff1.get_event_schedule(season, include_testing=False)
   #     schedule_list.append(schedule)
   # team_drivers = {}

   # for event in schedule_list:
    #    for _, event in schedule.iterrows():
    #        event_name = event["EventName"]
      #      try:
     #           race = ff1.get_session(season, event_name, "R")
      #          race.load(laps= False, telemetry=False, weather=False, messages=False)

           #     for _, row in race.results.iterrows():
              #      driver = row["Abbreviation"]
                #    team = row["TeamName"]

                    # Add driver to this team's set
                #    if team not in team_drivers:
                #        team_drivers[team] = set()
                  #  team_drivers[team].add(driver)


          #  except Exception as e:
            #    # Skip races that fail to load
              #  continue

  #  return {team: sorted(list(drivers)) for team, drivers in team_drivers.items()}



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
def get_tracks(season):
    schedule = ff1.get_event_schedule(season, include_testing=False)

    tracks_list = []

    for i, event in schedule.iterrows():
        tracks_list.insert(i, event["EventName"])
       
    return tracks_list
        


@st.cache_data
def get_track_stats(season, driver_code, trackname):
    pass
    #session = ff1.get_session(season,trackname, "R")
    #session.load(weather=False, messages=False)

   # stats = {
     #   "Races": 0,
     #   "Wins": 0,
     #   "Poles": 0,
     #   "Started": 0,
      #  "Finished": 0,
     #   "Avg_Lap_Time": [],
     #   "Sectors": []

   # }

   # results = session.results

   # driver_row = session.results[session.results["Abbreviation"] == driver_code]
   #if driver_row.empty:
    #    continue  # Driver didn't participate

    driver_row = driver_row.iloc[0]
    # Win
   # if driver_row["Position"] == 1:
     #   stats["Wins"] = 1


@st.cache_data
def get_driver_career_stats(driver_code):
    """Get aggregate career stats for a driver across all seasons"""
    seasons = get_available_seasons()

    career_stats = {
        "Seasons": 0,
        "Races": 0,
        "Points": 0,
        "Wins": 0,
        "Poles": 0,
        "DNFs": 0,
        "Teams": set(),
        "Best_Season": None,
        "Best_Points": 0,
    }

    season_breakdown = []

    for season in seasons:
        try:
            stats = get_driver_stats(season, driver_code)

            if stats["Races"] == 0:
                continue # Driver didn't race this season

            career_stats["Seasons"] += 1
            career_stats["Races"] += stats["Races"]
            career_stats["Points"] += stats["Points"]
            career_stats["Wins"] += stats["Wins"]
            career_stats["Poles"] += stats["Poles"]
            career_stats["DNFs"] += stats["DNFs"]

            if stats["Team"]:
                career_stats["Teams"].add(stats["Team"])

            if stats["Points"] > career_stats["Best_Points"]:
                career_stats["Best_Points"] = stats["Points"]
                career_stats["Best_Season"] = season

            season_breakdown.append({
                "Season": season,
                "Races": stats["Races"],
                "Points": stats["Points"],
                "Wins": stats["Wins"],
                "Poles": stats["Poles"],
                "DNFs": stats["DNFs"],
                "Team": stats["Team"],
            })

        except Exception:
            continue
    career_stats["Teams"] = sorted(list(career_stats["Teams"]))
    return career_stats, pd.DataFrame(season_breakdown)

@st.cache_data
def get_laps():
    pass


@st.cache_data
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



            if "Classified" in driver_row.index:
                is_dnf = not driver_row["Classified"]
                print(is_dnf)
            else:
                # fallback for the older seasons (pre-2000s) 
                # where 'Classified' might not exist in the API response.
                position = driver_row["Position"]
                status = driver_row.get("Status", "")
                is_dnf = (
                    pd.isna(position) or
                    position in ["DNF", "DNS", "DSQ", "NC"] or
                    status in ["DNF", "DNS", "DSQ", "Retired", "Accident", "Collision", "Engine", "Gearbox"]
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
