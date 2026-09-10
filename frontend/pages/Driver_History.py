import streamlit as st
import pandas as pd
from app.data_loader import *

# Get the stats of a driver which can be their overall stats, or stats based on a particularly individual season
# or a particularly track 

st.set_page_config(page_title="F1 Analytics", layout="wide")
st.title("🏎️ Driver Career Statistics")



seasons_list = get_available_seasons()



selected_season = st.sidebar.selectbox("Select an season", options=seasons_list, index=len(seasons_list) - 1)


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
driver_full_names = {}

for code in drivers_for_team:
    name = get_driver_full_name(code, selected_season)
    driver_full_names[code] = f"{code} - {name}"


driver_code = st.sidebar.selectbox(
    "Driver",
    options=drivers_for_team,
    format_func=lambda x: driver_full_names.get(x, x),
    index=0
)

if st.sidebar.button("Show  Stats"):
    with st.spinner("Calculating stats..."):
        stats = get_driver_stats(selected_season, driver_code)
        st.markdown(f"### 🏎️ {driver_code}")
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


#if selected == "Overall Season":
 #   pass

#elif selected == "Individual Season":
 #   with st.spinner(f"Loading data for {selected_season}..."):
  #          stats = get_driver_stats(selected_season, driver_code)
   #         st.markdown(f"### 🏎️ {driver_code}")
    #        st.metric("Team", stats["Team"])
     #       st.metric("Races", stats["Races"])
      #      st.metric("Points", stats["Points"])
       #     st.metric("Wins", stats["Wins"])
        #    st.metric("Poles", stats["Poles"])
         #   st.metric("DNFs", stats["DNFs"])
          #  if stats["Avg_Grid"]:
           #     st.metric("Avg Grid Position", f"{stats['Avg_Grid']:.1f}")
            #if stats["Avg_Finish"]:
             #   st.metric("Avg Finish Position", f"{stats['Avg_Finish']:.1f}")








#tab1, tab2, tab3 = st.tabs(["Overall", "Individual Season", "Individual Tracks"])


##with tab1:
 #   pass



#seasons = get_available_seasons()

#selected_season = st.selectbox("Select a Season", options=seasons, index=len(seasons) - 1)

#with st.spinner(f"Loading data for {selected_season}..."):
   # team_drivers = get_season_teams_and_drivers(selected_season)
    #if not team_drivers:
     #       st.error(f"No data available for {selected_season}. Try a different season.")
      #      st.stop()


#available_teams = sorted(list(team_drivers.keys()))
#selected_team = st.selectbox(
 #       "Select Team",
  #      options=available_teams
   # )

#drivers_for_team = team_drivers[selected_team]
#driver_full_names = {}
#for code in drivers_for_team:
 #       name = get_driver_full_name(code, selected_season)
  #      driver_full_names[code] = f"{code} - {name}"





#with tab2:
    #if st.button("Show  Stats"):
     #   #with st.spinner("Calculating stats..."):
      #      stats = get_driver_stats(selected_season, driver_code)
#
 #       st.metric("Team", stats["Team"])
  #      st.metric("Races", stats["Races"])
    #    st.metric("Points", stats["Points"])
   #     st.metric("Wins", stats["Wins"])
     #   st.metric("Poles", stats["Poles"])
      #  st.metric("DNFs", stats["DNFs"])
       # if stats["Avg_Grid"]:
        #    st.metric("Avg Grid Position", f"{stats['Avg_Grid']:.1f}")
        #if stats["Avg_Finish"]:
         #   st.metric("Avg Finish Position", f"{stats['Avg_Finish']:.1f}")


        


#with tab3:
   # available_tracks = get_tracks(selected_season)
   # selected_track = st.selectbox("Select a track", options= available_tracks, index=0)

  #  if st.button("Show Stats"):
        #with st.spinner("Calculating stats..."):
    #        stats = get_track_stats(selected_season, driver_code, selected_track)

      #  st.markdown(f"### 🏎️ {selected_track}")

