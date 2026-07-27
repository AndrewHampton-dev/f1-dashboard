import streamlit as st
import pandas as pd
import numpy as np
from numpy.random import default_rng as rng

st.set_page_config(page_title="F1 Analytics", layout="wide")
st.title("🏎️ Head-to-Head records")


Season_list = ["2026", "2025", "2024", "2023"]



drivers_list = ["Max Verstappen", "Isack Hadjar", "Valtteri Bottas", 
    "Lewis Hamilton", "Lando Norris","Oscar Piastri"]


driver1 = st.selectbox("Please select the first driver", drivers_list)

driver2 = st.selectbox("Please select the second driver", drivers_list)

Season = st.selectbox("Please select a season", Season_list)




metrics = [
    "Points",
    "Race Results",      # e.g., average finishing position or recent finishes
    "Qualifying",        # e.g., average grid position
    "Fastest Lap",       # number of fastest laps
    "Laps in Top 10",    # percentage or count
    "Best Results"       # e.g., number of wins/podiums
]

# 3. Create the data for each column (must be in the same order as 'metrics')
data = {
    driver1: [245, "1st, 3rd, 2nd", "P1, P2, P3", 4, "85%", "3 wins"],
    driver2: [210, "2nd, 4th, 1st", "P3, P1, P5", 2, "78%", "2 wins"],
    "Winner": ["Verstappen", "Verstappen", "Hamilton", "Verstappen", "Verstappen", "Verstappen"]
}


cd = pd.DataFrame(rng(0).standard_normal((20, 3)), columns=[Season, driver1, driver2])


chart_list = [
    "Points",
    "Race Results",
    "Qualifying"
]

chart_options= st.selectbox("Select a chart",chart_list)

if chart_options == "Points":
        st.line_chart(
        cd,
        x=Season,
        y=[driver1, driver2],
        color=["#FF0000", "#0000FF"],
        y_label="Points"
    )



# 4. Build the DataFrame with the metrics as the row index
df = pd.DataFrame(data, index=metrics)

styled_df = df.style.applymap(
    lambda x: 'font-weight: bold; colour: green;' if x in ['Verstappen', 'Hamilton'] else '', 
    subset='Winner'
)

# 5. Display it in Streamlit
st.dataframe(styled_df, width="stretch")