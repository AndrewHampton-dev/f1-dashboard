import streamlit as st
import pandas as pd

st.set_page_config(page_title="F1 Analytics", layout="wide")
st.title("🏎️ Formula 1 stats Dashboard")

# Mock Data (Replace with API calls later)
mock_standings = [{"Position": 1, "Driver": "Max Verstappen", "Team": "Red Bull", "Points": 255},
    {"Position": 2, "Driver": "Lando Norris", "Team": "McLaren", "Points": 198},
    {"Position": 3, "Driver": "Charles Leclerc", "Team": "Ferrari", "Points": 177},]


mock_constructor_standings = [{"Position": 1, "Team": "Aston Martian", "Points": 255},
    {"Position": 2, "Team": "McLaren", "Points": 198},
    {"Position": 3, "Team": "Ferrari", "Points": 177},]


df = pd.DataFrame(mock_standings)

cdf = pd.DataFrame(mock_constructor_standings)


col1, col2, col3 = st.columns(3)
col1.metric("Current Leader", "Max Verstappen", "Red Bull")
col2.metric("Closest Challenger", "Lando Norris", "-57 pts")
col3.metric("Races Remaining", "10", "Next: Spa")

st.subheader("Driver Standings")
st.dataframe(df, width="stretch", hide_index=True)

c1, c2,c3 = st.columns(3)
col1.metric("Current Leader", "Aston Martian")
col2.metric("Closest Challenger", "McLaren", "-57 pts")
col3.metric("Races Remaining", "10", "Next: Spa")

st.subheader("Constrcutor Standings")
st.dataframe(cdf, width="stretch", hide_index=True)
