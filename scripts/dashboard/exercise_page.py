import streamlit as st
# from scripts.database import FitbitDatabase
# import sys
# import os
# import numpy as np
import pandas as pd
# import plotly.express as px
from scripts.dashboard.diagrams.exercise_diagrams import ExerciseDiagrams

@st.cache_resource
def get_exercise_diagrams():
    return ExerciseDiagrams(st.session_state["fitbit_db"], "data/chicago_data.csv")
diagrams = get_exercise_diagrams()

user = st.session_state["selected-user"]
start_date = pd.to_datetime(st.session_state["selected-start-date"])
end_date = pd.to_datetime(st.session_state["selected-end-date"])

st.title("Exercise")
col1, col2 = st.columns(2)
with col1:
    if user == "All":
        st.plotly_chart(diagrams.plot_distance_walked_density())
    else:
        st.plotly_chart(diagrams.plot_steps_to_calories_regression(user))

with col2:
    if user == "All":
        st.plotly_chart(diagrams.plot_day_of_week_frequency())
        
# st.plotly_chart(diagrams.plot_weather_correlation_for_chicago())
