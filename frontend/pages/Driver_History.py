import streamlit as st
import pandas as pd
from numpy.random import default_rng as rng

# Get the stats of a driver which can be their overall stats, or stats based on a particularly individual season
# or a particularly track 

def overall(season):
    pass

def individual_season(season):
    pass
def individual_track(season, track):
    pass

st.set_page_config(page_title="F1 Analytics", layout="wide")
st.title("🏎️ Driver History records")

tab1, tab2, tab3 = st.tabs(["Overall", "Individual Season", "Individual Tracks"])

