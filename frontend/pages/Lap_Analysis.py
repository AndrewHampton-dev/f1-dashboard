import streamlit as st
import fastf1
import pandas as pd
from app.data_loader import *
from fastf1 import plotting
import matplotlib
from matplotlib.ticker import FuncFormatter
from app.data_loader import *

matplotlib.use('TkAgg')

from matplotlib import pyplot as plt

st.set_page_config(page_title="F1 Analytics", layout="wide")
st.title("🏎️ Lap & Sector Analysis")

fastf1.plotting.setup_mpl(
    mpl_timedelta_support=True,
    color_scheme='fastf1'
)


season = st.sidebar.selectbox("Season", get_available_seasons(), index=len(get_available_seasons()) - 1)

schedule = get_season_schedule(season)



event = schedule["EventName"].tolist()

selected_track = st.sidebar.selectbox("Track", event)


# Get all laps for a single driver
def get_driver_lap_time(session, driver):
    return session.laps.pick_drivers(driver)

if season >= 2018:
    session = fastf1.get_session(season, selected_track, 'R')
    session.load(laps=True, telemetry=True)
    
    driver_list = session.results['Abbreviation'].tolist()


    laps_list = session.laps

    tab1, tab2 = st.tabs(["Lap Analytics", "Sector Analytics"])

    with tab1:
        st.header("Lap Analytics")
        selected_drivers = st.sidebar.multiselect(
            "Select a driver",
            options=driver_list,

        )
      

        lap_numbers = laps_list['LapNumber'].astype(int).tolist()



        selected_lap = st.sidebar.multiselect("One or more Laps", options=lap_numbers)
        

        if st.button("Show drivers quicklaps"):
            fig, ax = plt.subplots(figsize=(8, 5))
            if selected_drivers:
                for driver in selected_drivers:
                    driver_laps = session.laps.pick_drivers(driver).pick_quicklaps()
                    driver_laps = driver_laps.reset_index()

                    driver_laps["LapTimeSeconds"] = driver_laps["LapTime"].dt.total_seconds()

                    style = plotting.get_driver_style(
                        identifier= driver,
                        style=['color', 'linestyle'],
                        session=session
                    )
                    ax.plot(driver_laps['LapNumber'], driver_laps['LapTime'], 
                        **style, label=driver)



                ax.yaxis.set_major_formatter(FuncFormatter(racing_time_formatter))

                ax.set_title("Drivers' Quick Laps Timeline", fontsize=14, pad=15)
                ax.set_xlabel("Lap Number", fontsize=11)
                ax.set_ylabel("Lap Time (MM:SS.mmm)", fontsize=11)
                ax.invert_yaxis() 
                ax.grid(axis='x', linestyle='--', alpha=0.4)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.legend(frameon=False, loc='best')

                st.pyplot(fig)
                plt.close(fig)

            elif not selected_drivers:
                st.warning("No driver selected yet.")
        if st.button("Show specific laps"):
            fig, ax = plt.subplots(figsize=(8, 5))
            if selected_drivers and selected_lap:
                for driver in selected_drivers:

                    driver_laps = session.laps.pick_drivers(driver).pick_laps(selected_lap)
                    driver_laps = driver_laps.reset_index()

                    driver_laps.pick_track_status()

                    if driver_laps.empty:
                        continue

                    color_driver = fastf1.plotting.get_team_color(driver_laps['Team'].iloc[0], session)

                    style = plotting.get_driver_style(
                        identifier= driver,
                        style=['color', 'linestyle'],
                        session=session
                    )

                    ax.plot(driver_laps["LapNumber"], driver_laps['LapTime'], 
                            label=f"{driver} (Lap {selected_lap})", **style)

                ax.yaxis.set_major_formatter(FuncFormatter(racing_time_formatter))
                ax.set_title("Drivers' Specific Laps Times", fontsize=14, pad=15)
                ax.set_xlabel("Lap Number", fontsize=11)
                ax.set_ylabel("Lap Time (MM:SS.mmm)", fontsize=11)
                ax.invert_yaxis() 
                ax.grid(axis='x', linestyle='--', alpha=0.4)
                ax.legend(frameon=False, loc='best')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                st.pyplot(fig)
                plt.close(fig)

            elif not selected_drivers:
                st.warning("No drivers selected yet.")
            elif not selected_lap:
                st.warning("No laps selected yet.")



        with tab2:
            #fig, ax = plt.subplots(figsize=(8, 5))
            if st.button("Show Sector Times"):
                if selected_drivers:
                    all_sectors_data = []
                    missing_drivers = []  # Track drivers with DNS/DNF/No Telemetry
                    for driver in selected_drivers:

                        try:
                            laps = session.laps.pick_drivers(driver)

                            laps = laps.dropna(subset=['Sector1Time', 'Sector2Time', 'Sector3Time'])

                            if laps.empty:
                                missing_drivers.append(driver)  # Track drivers with DNS/DNF/No Telemetry
                                continue

                            laps["Sector1Time(s)"] = laps["Sector1Time"].dt.total_seconds()
                            laps["Sector2Time(s)"] = laps["Sector2Time"].dt.total_seconds()
                            laps["Sector3Time(s)"] = laps["Sector3Time"].dt.total_seconds()
                            laps["LapTime"] =        laps["LapTime"].dt.total_seconds()

                            ideal_lap = laps.pick_quicklaps()
                            if ideal_lap.empty:
                                missing_drivers.append(driver)
                                continue

                            # --- Calculate Theoretical Ideal Sectors ---
                            ideal_s1 =  ideal_lap["Sector1Time(s)"].min()
                            ideal_s2 =  ideal_lap["Sector2Time(s)"].min()
                            ideal_s3 =  ideal_lap["Sector3Time(s)"].min()

                            # --- Calculate Actual Best Lap Sectors ---
                            fastest_lap = laps.pick_fastest() 

                            if fastest_lap.empty:
                                missing_drivers.append(driver)
                                continue

                            actual_s1 = fastest_lap["Sector1Time(s)"].item()
                            actual_s2 = fastest_lap["Sector2Time(s)"].item()
                            actual_s3 = fastest_lap["Sector3Time(s)"].item()

                            # --- Total Lap Time ---
                            total_lap_time = laps["LapTime"].min()

                            print(total_lap_time)
                            all_sectors_data.append({
                                "Driver": driver, 
                                ("Actual Best Lap", "Sector 1"): actual_s1,
                                ("Actual Best Lap", "Sector 2"): actual_s2,
                                ("Actual Best Lap", "Sector 3"): actual_s3,
                                ("Theoretical Ideal","Sector 1"): ideal_s1, 
                                ("Theoretical Ideal","Sector 2"): ideal_s2,  
                                ("Theoretical Ideal","Sector 3"): ideal_s3, 
                                ("Total Lap Time", "Time"): total_lap_time


                            })
                        except Exception as e:
                            print(f"Error processing driver {driver}: {e}")
                            missing_drivers.append(driver)
                            continue


                    if all_sectors_data:

                        sectors_df =  pd.DataFrame(all_sectors_data)
                        sectors_df.set_index("Driver", inplace=True)
                        sectors_df.columns = pd.MultiIndex.from_tuples(sectors_df.columns)
                        st.subheader("Sector Times Comparison")

                        st.table(sectors_df, height="content")
                    else:
                         st.warning("No data available for the selected drivers.")

                    if missing_drivers:
                        drivers_str = ",".join(missing_drivers)
                        st.warning(f"⚠️ No lap telemetry found for: **{drivers_str}**. They may have DNF'd, DNS'd, or lacked timing data.")




     #   with tab3:
     #       pass
            #if selected_drivers:
                #fig, ax = plt.subplots(figsize=(12, 6))
                #for driver in selected_drivers:
                    #driver_laps = session.laps.pick_drivers(driver)
                    #driver_laps['LapTimeSeconds'] = driver_laps['LapTime']
                    #in_laps = driver_laps[~driver_laps["PitInTime"].isna()]
                    #out_laps = driver_laps[~driver_laps["PitOutTime"].isna()]


                    #in_laps["PitInTime"] = in_laps["PitInTime"].dt.total_seconds()
                    #out_laps["PitOutTime"] = out_laps["PitOutTime"].dt.total_seconds()

                    #normal_laps = driver_laps[driver_laps['PitInTime'].isna() & driver_laps['PitOutTime'].isna()]
                    #Plot the continuous baseline race stint trend line
                   # ax.plot(driver_laps['LapNumber'], driver_laps['LapTimeSeconds'], color='white', alpha=0.3, linestyle='--')

                  #  ax.scatter(normal_laps['LapNumber'], normal_laps['LapTimeSeconds'], color='cyan', label='Normal Laps', s=30)
                 #   ax.scatter(in_laps['LapNumber'], in_laps['LapTimeSeconds'], color='red', marker='v', label='In-Lap (Pitting In)', s=80)
               #     ax.scatter(out_laps['LapNumber'], out_laps['LapTimeSeconds'], color='lime', marker='^', label='Out-Lap (Pitting Out)', s=80)
                #ax.set_title(f"{session.event['EventName']} 2024 - {driver} Pit Stop & Lap Evaluation")
             #   ax.set_xlabel("Lap Number")
              #  ax.set_ylabel("Lap Time (Seconds)")
             #   ax.legend()
             #   ax.grid(True, alpha=0.2)
#
              #  plt.show()

else:
        st.warning(f"Telemetry and detailed lap data are only available from 2018 onwards. Showing historical database results for {season}.")

        tab4, tab5 = st.tabs(["Race Results", "Season Standings"])
    
        with tab3:
            pass

        with tab4:
            pass
                


