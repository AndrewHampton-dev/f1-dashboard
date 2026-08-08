import streamlit as st
import fastf1 as ff1 

@st.cache_data
def load_race_session(season, round_number):
	schedule = ff1.get_event_schedule(season)
	event = schedule[schedule["RoundNumber"] == "round_number"].iloc[0]
	session = ff1.get_session(season, event["EventName"], "R")

	session.load(laps=False, telemetry=False, weather=False, messages=False)

@st.cache_data
def load_quali_session(season, round_number):
    """Load qualifying session for a race"""
    schedule = ff1.get_event_schedule(season)
    event = schedule[schedule["RoundNumber"] == round_number].iloc[0]
    try:
        session = ff1.get_session(season, event["EventName"], "Q")
        session.load(laps=False, telemetry=False, weather=False, messages=False)
        return session
    except:
        return None  # Some races don't have qualifying (e.g., old seasons)