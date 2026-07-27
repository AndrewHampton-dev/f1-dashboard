import streamlit as st
import pandas as pd

st.set_page_config(page_title="F1 Analytics", layout="wide")
st.title("🏎️ Track History records")

Season_list = ["2026", "2025", "2024", "2023"]
Season = st.selectbox("Please select a season", Season_list)

track_list = ["Monza GP", "Las Vega GP","Montrel GP", "Mexcian GP", "Interlagos GP", "Silverstone GP"]

track = st.selectbox("Please select a track", track_list)

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
	track: ["Monza 2025 GP", 1921, " Michael Schumacher and Lewis Hamilton", "Ferrari (21)", "5.793 km (3.600 miles)", 
	"369,0x041", "Max Verstappen (Red Bull)", "1:18.792", "Lando Norris (McLaren)",
	 "1:20.901", "1st Max Verstappen, 2nd Lando Norris, 3rd Oscar Piastri "]
}

df = pd.DataFrame(data, index=metrics)

st.dataframe(df, width="stretch")