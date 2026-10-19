import streamlit as st
import fastf1
from fastf1 import plotting
import pandas as pd
from app.data_loader import *
from matplotlib import pyplot as plt

st.set_page_config(page_title="F1 Analytics", layout="wide")
st.title("🏎️ Season comparison Statistics")

fastf1.plotting.setup_mpl(
    mpl_timedelta_support=True,
    color_scheme='fastf1'
)


seasons_list = get_available_seasons()


seasons_sorted = sorted(seasons_list,reverse=True)

selected_seasons = st.sidebar.multiselect(
            "Select season", 
            options=seasons_sorted,
            max_selections=2,
            select_all= False
)

schedule_list = []

event = []

for index, season in enumerate(selected_seasons):
    schedule_list.append(get_season_schedule(season))

    event = schedule_list[index]["EventName"]
if not selected_seasons:
    st.error(f"No seasons has been selected")
    st.stop()


team_drivers = get_season_teams_and_drivers(selected_seasons[0])

if not team_drivers:
    st.error(f"No data available for {selected_seasons[0]}. Try a different season.")
    st.stop()

available_teams = sorted(list(team_drivers.keys()))
selected_team = st.sidebar.selectbox(
        "Select Team",
        options=available_teams
    )

drivers_for_team = team_drivers[selected_team]
driver_full_names = {}

for code in drivers_for_team:
    name = get_driver_full_name(code, selected_seasons[0])
    driver_full_names[code] = f"{code} - {name}"


driver_code = st.sidebar.selectbox(
    "Driver",
    options=drivers_for_team,
    format_func=lambda x: driver_full_names.get(x, x),
    index=0
)

if st.sidebar.button("Show  Stats"):
    with st.spinner("Calculating stats..."):
        for index, season in enumerate(selected_seasons):

            stats = get_driver_stats(selected_seasons[index], driver_code)
            st.markdown(f"### 🏎️ {driver_code} Season {selected_seasons[index]}")
            st.metric("Team", stats["Team"])
            st.metric("Races", stats["Races"])
            st.metric("Points", stats["Points"])
            st.metric("Wins", stats["Wins"])
            st.metric("Poles", stats["Poles"])
            st.metric("DNFs", stats["DNFs"])
            if stats["Avg_Grid"]:
                  st.metric("Avg Grid Position", f"{stats['Avg_Grid']:.1f}")
            if stats["Avg_Finish"]:
                  st.metric("Avg Finish Position", f"{stats['Avg_Finish']:.1f}")


