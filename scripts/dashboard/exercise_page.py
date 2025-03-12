import streamlit as st
from scripts.database import FitbitDatabase
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append(os.path.join(os.getcwd(), "diagrams"))
import exercise_diagrams
fitbit_db: FitbitDatabase = st.session_state["fitbit_db"]
user = st.session_state["selected_user"]
start_date = pd.to_datetime(st.session_state["selected-start-date"])
end_date = pd.to_datetime(st.session_state["selected-end-date"])

st.title("Exercise")
col1, col2 = st.columns(2)
with col1:
    data = fitbit_db.get_daily_activity()
    if(user == "All"):
        st.pyplot(exercise_diagrams.plot_distance_walked_density(data))
    else:
        st.pyplot(exercise_diagrams.plot_calories_burned(data, user, start_date, end_date))

    
    
    
