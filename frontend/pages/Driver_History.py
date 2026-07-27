import streamlit as st
import pandas as pd
from numpy.random import default_rng as rng

st.set_page_config(page_title="F1 Analytics", layout="wide")
st.title("🏎️ Driver History records")

Season_list = ["2026", "2025", "2024", "2023"]

Season = st.selectbox("Please select a season", Season_list)

drivers_list = ["Max Verstappen", "Isack Hadjar", "Valtteri Bottas", 
    "Lewis Hamilton", "Lando Norris","Oscar Piastri"]


driver = st.selectbox("Please select a driver", drivers_list)


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

# 3. Create the data for each column (must be in the same order as 'metrics')
data = {
    driver: [4, 10, 30, 245, "1st", "P1", 4, "85%", "3 wins"],
}

cd = pd.DataFrame(rng(0).standard_normal((20, 2)), columns=[Season, driver])


chart_list = [
    "Points",
    "Race Results",
    "Qualifying"
]

chart_options= st.selectbox("Select a chart",chart_list)

if chart_options == "Points":
        st.line_chart(
        cd,
        x=Season,
        y=driver,
        color=["#FF0000"],
        y_label="Points"
    )


df = pd.DataFrame(data, index=metrics)

st.dataframe(df, width="stretch")