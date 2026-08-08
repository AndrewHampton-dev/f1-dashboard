import streamlit as st
import pandas as pd
from fastapi import FastAPI
import fastf1
from fastf1.ergast import Ergast
from datetime import datetime


st.set_page_config(page_title="F1 Analytics", layout="wide")
st.title("🏎️ Formula 1 Stats Dashboard")

ergast = Ergast()
current_year = datetime.now().year

st.subheader("Current Championships Standings")

driver_df = ergast.get_driver_standings(current_year).content[0]

constructor_df = ergast.get_constructor_standings(current_year).content[0]


driver_df['fullName'] = driver_df['givenName'] + ' ' + driver_df['familyName']

driver_df = driver_df[
    ["position", "fullName", "points", "wins"]
    
].rename(columns={
    "position": "Position",
    "fullName": "FullName",
    "points": "Points",
    "wins": "Wins"

})

constructor_df = constructor_df[
    ["position", "constructorName", "points", "wins"]
].rename(columns={
    "position": "Position",
    "constructorName": "Constructor",
    "points": "Points",
    "wins": "Wins"
})

c1, c2, c3 = st.columns(3)

constructor_standings = [{"Position": constructor_df.iloc[0]["Position"], "Team": constructor_df.iloc[0]["Constructor"], 
    "Points":constructor_df.iloc[0]["Points"], "Wins":constructor_df.iloc[0]["Wins"] },
    {"Position": constructor_df.iloc[1]["Position"], "Team": constructor_df.iloc[1]["Constructor"], 
    "Points": constructor_df.iloc[1]["Points"],  "Wins":constructor_df.iloc[1]["Wins"]},
    {"Position": constructor_df.iloc[2]["Position"], "Team": constructor_df.iloc[2]["Constructor"], 
    "Points": constructor_df.iloc[2]["Points"],  "Wins":constructor_df.iloc[2]["Wins"]},]

col1, col2, col3 = st.columns(3)
driver_standings = [
    {"Position":  driver_df.iloc[0]["Position"], 
    "FullName": driver_df.iloc[0]["FullName"], "Wins":driver_df.iloc[0]["Wins"]},
    {"Position":  driver_df.iloc[1]["Position"],
    "FullName": driver_df.iloc[1]["FullName"], "Points": driver_df.iloc[1]["Points"], "Wins":driver_df.iloc[1]["Wins"]},
    {"Position":  driver_df.iloc[2]["Position"],
    "FullName": driver_df.iloc[2]["FullName"], "Points": driver_df.iloc[2]["Points"], "Wins":driver_df.iloc[2]["Wins"]}
    ]


df = pd.DataFrame(driver_standings)

cdf = pd.DataFrame(constructor_standings)

remaining_races = fastf1.get_events_remaining(include_testing=False)
num_remaining  = len(remaining_races)

dif = constructor_df.iloc[0]["Points"] - constructor_df.iloc[1]["Points"]

num = str(dif)

next_race = str(remaining_races.iloc[0]["Location"])

c1, c2,c3 = st.columns(3)
c1.metric("Current Leader",  constructor_df.iloc[0]["Constructor"], num)
c2.metric("Closest Challenger",  constructor_df.iloc[1]["Constructor"], "-" + num)
c3.metric("Races Remaining", num_remaining, "Next: " + next_race)

dif = driver_df.iloc[0]["Points"] - driver_df.iloc[1]["Points"]

col1, col2,col3 = st.columns(3)

num = str(dif)

col1.metric("Current Leader",  driver_df.iloc[0]["FullName"], num)
col2.metric("Closest Challenger",  driver_df.iloc[1]["FullName"], "-" + num)


st.subheader("Constructor Championships Standings")
st.dataframe(cdf, width="stretch", hide_index=True)

st.subheader("Driver Championships Standings")
st.dataframe(df, width="stretch", hide_index=True)

