import streamlit as st
import fastf1
from datetime import date
import tempfile
import os
import numpy as np
import pandas as pd
current_year = date.today().year


st.title("F1 stats Dashboard")
st.header("")


project_cache = os.path.join(os.getcwd(), 'fastf1_cache')

st.write("Please choose a driver to see their stats")

driver = st.sidebar.selectbox("select a driver:", ["Lando Norris", "Max Verstappen", "Lewis Hamilton"])

team = st.sidebar.selectbox("Select a team: ", ["Ferrari", "Red Bull", "McLaren"])

driver_button = st.sidebar.button("Select a driver")

team_button = st.button("Select a team")

if driver_button:
	st.write("You have a selected a driver")
race = fastf1.get_session(current_year, 1,'R')

if team_button:
	st.write("You have selected a team")

race.load()

alonso_laps = race.laps.pick_drivers('ALO')

chart_data = pd.DataFrame(np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)






#def __main__():
	#Faster sebsequent loads

#	print(race)

#if __name__ == "__main__":
#	__main__()
