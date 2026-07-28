import streamlit as st
import pandas as pd
from numpy.random import default_rng as rng

st.set_page_config(page_title="F1 Analytics", layout="wide")
st.title("🏎️ Driver History records")


driver_teams_by_season = {
    "2023": {"Red Bull": ["Verstappen", "Perez"], "Mercedes": ["Hamilton", "Russell"]},
    "2024": {"Red Bull": ["Verstappen", "Perez"], "Ferrari": ["Leclerc", "Sainz"]}
}


season = st.selectbox("Select a season", options= list(driver_teams_by_season.keys()))

team = st.selectbox("Select a team", options= driver_teams_by_season[season].keys(), index=0)

driver = st.selectbox("Please select the first driver", driver_teams_by_season[season][team])



metrics = [
    "Championships",
    "Race wins",
    "Pole",
    "Points",
    "Race Results",      # e.g., average finishing position or recent finishes
    "Qualifying",        # e.g., average grid position
    "Fastest Lap",       # number of fastest laps
    "Laps in Top 10",    # percentage or count
    "Best Results"       # e.g., number of wins/podiums
]

data = {
    driver: [4, 10, 30, 245, "1st", "P1", 4, "85%", "3 wins"],
}

wins_cd = pd.DataFrame(rng(0).standard_normal((20, 2)), columns=[season, driver])

podium_cd = pd.DataFrame(rng(0).standard_normal((20, 2)), columns=[season, driver])

pole_cd = pd.DataFrame(rng(0).standard_normal((21, 2)), columns=[season, driver])
points_cd = pd.DataFrame(rng(0).standard_normal((20, 2)), columns=[season, driver])
race_results = pd.DataFrame(rng(0).standard_normal((22, 2)), columns=[season, driver])
qualifying = pd.DataFrame(rng(0).standard_normal((22, 2)), columns=[season, driver])

chart_list = [
    "Wins",
    "Podium",
    "Pole",
    "Points",
    "Race Results",
    "Qualifying"
]

chart_options= st.selectbox("Select a chart",chart_list)

if chart_options == "Wins":
        st.line_chart(
        wins_cd,
        x=season,
        y=driver,
        color=["#FF0000"],
        y_label="Wins"
    )
elif chart_options == "Podium":
        st.line_chart(
        podium_cd,
        x=season,
        y=driver,
        color=["#FF0000"],
        y_label="Podium"
    )
elif chart_options == "Pole":
    st.line_chart(
        pole_cd,
        x=season,
        y=driver,
        color=["#FF0000"],
        y_label="Pole"
    )
elif chart_options == "Points":
        st.line_chart(
        points_cd,
        x=season,
        y=driver,
        color=["#FF0000"],
        y_label="Points"
    )
elif chart_options == "Race Results":
        st.line_chart(
        points_cd,
        x=season,
        y=driver,
        color=["#FF0000"],
        y_label="race_results"
    )
elif chart_options == "Qualifying":
        st.line_chart(
        points_cd,
        x=season,
        y=driver,
        color=["#FF0000"],
        y_label="Qualifying"
    )


df = pd.DataFrame(data, index=metrics)

st.dataframe(df, width="stretch")