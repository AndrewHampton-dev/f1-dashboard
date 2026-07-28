import streamlit as st
import pandas as pd

st.set_page_config(page_title="F1 Analytics", layout="wide")
st.title("🏎️ Track History records")

tracks_by_seasons={
	"2023": ["Monza", "Spa", "Monaco"],
	"2024": ["Silverstone", "Montreal", "Interlagos"]
}

season = st.selectbox("Please select a season", list(tracks_by_seasons.keys()), index=0)



track = st.selectbox("Please select a track", options= tracks_by_seasons[season])

metrics = [
	"Course Name",
	"First held",
	"Most Wins (drivers)",
	"Most Wins (Constructor)",
	"Course length",
	"Attendance",
	"pole position",
	"pole_lap_time",
	"Fastest_lap",
	"Fastest_time",
	"Podium"
]

data = {
	track: ["Monza GP", 1921, " Michael Schumacher and Lewis Hamilton", "21 (Ferrari)", "5.793 km (3.600 miles)", 
	"369,041", "Max Verstappen (Red Bull)", "1:18.792", "Lando Norris (McLaren)",
	 "1:20.901", "1st Max Verstappen, 2nd Lando Norris, 3rd Oscar Piastri "]
}

df = pd.DataFrame(data, index=metrics)

st.dataframe(df, width="stretch")