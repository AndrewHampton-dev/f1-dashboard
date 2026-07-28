import streamlit as st
import pandas as pd
import numpy as np
from numpy.random import default_rng as rng

st.set_page_config(page_title="F1 Analytics", layout="wide")
st.title("🏎️ Head-to-Head records")


driver_teams_by_season = {
    "2023": {"Red Bull": ["Verstappen", "Perez"], "Mercedes": ["Hamilton", "Russell"]},
    "2024": {"Red Bull": ["Verstappen", "Perez"], "Ferrari": ["Leclerc", "Sainz"]}
}


season = st.selectbox("Select a season", options= list(driver_teams_by_season.keys()))

team = st.selectbox("Select a team", options= driver_teams_by_season[season].keys(), index=0)

driver1 = st.selectbox("Please select the first driver", driver_teams_by_season[season][team])

driver2 = st.selectbox("Please select the second driver", driver_teams_by_season[season][team])

st.write(f"You selected **{team}** from the **{season}** season.")



metrics = [
    "Points",
    "Race Results",      # e.g., average finishing position or recent finishes
    "Qualifying",        # e.g., average grid position
    "Fastest Lap",       # number of fastest laps
    "Laps in Top 10",    # percentage or count
    "Best Results"       # e.g., number of wins/podiums
]

# 3. Create the data for each column (must be in the same order as 'metrics')
data = {
    driver1: [245, "1st, 3rd, 2nd", "P1, P2, P3", 4, "85%", "3 wins"],
    driver2: [210, "2nd, 4th, 1st", "P3, P1, P5", 2, "78%", "2 wins"],
    "Winner": ["Verstappen", "Verstappen", "Hamilton", "Verstappen", "Verstappen", "Verstappen"]
}


cd = pd.DataFrame(rng(0).standard_normal((20, 3)), columns=[season, driver1, driver2])


chart_list = [
    "Points",
    "Race Results",
    "Qualifying"
]

chart_options= st.selectbox("Select a chart",chart_list)

if chart_options == "Points":
        st.line_chart(
        cd,
        x=season,
        y=[driver1, driver2],
        color=["#FF0000", "#0000FF"],
        y_label="Points"
    )



df = pd.DataFrame(data, index=metrics)

styled_df = df.style.applymap(
    lambda x: 'font-weight: bold; colour: green;' if x in ['Verstappen', 'Hamilton'] else '', 
    subset='Winner'
)

st.dataframe(styled_df, width="stretch")