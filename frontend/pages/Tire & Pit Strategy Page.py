import streamlit as st
import fastf1
import pandas as pd
from app.data_loader import *
from fastf1 import plotting
import matplotlib
from matplotlib.ticker import FuncFormatter
from app.data_loader import *

matplotlib.use('Agg')

from matplotlib import pyplot as plt


st.set_page_config(page_title="F1 Analytics", layout="wide")
st.title("🏎️ Tire & Strategy Page")

fastf1.plotting.setup_mpl(
    mpl_timedelta_support=True,
    color_scheme='fastf1'
)


season = st.sidebar.selectbox("Season", get_available_seasons(), index=len(get_available_seasons()) - 1)

schedule = get_season_schedule(season)



event = schedule["EventName"].tolist()

selected_track = st.sidebar.selectbox("Track", event)


session = fastf1.get_session(season, selected_track, 'R')
session.load(laps=True, telemetry=True)
    
driver_list = session.results['Abbreviation'].tolist()


laps_list = session.laps

selected_drivers = st.sidebar.multiselect(
    "Select a driver",
    options=driver_list,

)
 

if st.button("Pit Stop Duration"):
    if selected_drivers:
        pass

if st.button("Show Tire compound"):
    fig, ax = plt.subplots(figsize=(8, 5))
    if selected_drivers:
        for driver in selected_drivers:

            # Track the starting lap position across sequential stints
            current_start_lap = 1 
            driver_laps = session.laps.pick_drivers(driver)

            for stint in driver_laps['Stint'].unique():
                stint_laps = driver_laps[driver_laps["Stint"] == stint]
                compound = stint_laps.iloc[0]['Compound']
                num_laps = len(stint_laps)
                color = fastf1.plotting.get_compound_color(compound, session=session)

                ax.barh(

                    y=driver, 
                    width=num_laps, 
                    left=current_start_lap, 
                    color=color, 
                    edgecolor="black", 
                    height=0.5
                )



                current_start_lap += num_laps


            ax.set_title("Race Tire Strategy Timeline", fontsize=14, pad=15)
            ax.set_xlabel("Lap Number", fontsize=11)
            ax.set_ylabel("Driver", fontsize=11)

            # Invert y-axis to stack drivers top-to-bottom in selection order
        ax.invert_yaxis() 
        ax.grid(axis='x', linestyle='--', alpha=0.4)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close(fig)



    elif not selected_drivers:
        st.warning("No driver selected yet.")

if st.button("Tire Life"):
    if selected_drivers:

        for driver in selected_drivers:
            driver_tyre = session.laps.pick_drivers(driver)
            current_start_lap = 1 
            for stint in driver_tyre["TyreLife"].unique()
                stint_laps = driver_laps[driver_laps["Stint"] == stint]
                trye_life = driver_tyre.iloc[0]['TyreLife']
                num_laps = len(stint_laps)
                color = fastf1.plotting.get_compound_color(trye_life, session=session)
                ax.barh(
                    y=driver,
                    width=num_laps
                )

                




