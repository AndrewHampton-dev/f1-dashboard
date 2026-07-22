import streamlit as st
from datetime import date
import tempfile
import os

#current_year = date.today().year
#print(current_year)
#st.title("F1 stats Dashboard")
#st.header("")



#st.write("Please choose a driver to see their stats")

#driver = st.selectbox("select a driver:", ["Lando Norris", "Max Verstappen", "Lewis Hamilton"])

#driver_button = st.button("Select a driver")

#if driver_button:
#	st.write("You have a selected a driver")

#race = fastf1.get_session(current_year, 1,'R')



#race.load()

class StreamitApp:
	pass



def __main__():
	#Faster sebsequent loads
	project_cache = os.path.join(os.getcwd(), 'fastf1_cache')

	race = session.get_race
	print(race)

if __name__ == "__main__":
	__main__()
