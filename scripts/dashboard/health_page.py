import streamlit as st
import pandas as pd

from scripts.dashboard.diagrams.health_diagrams import HealthDiagrams

health_diagrams = HealthDiagrams(st.session_state["fitbit_db"])
user = st.session_state["selected-user"]
start_date = pd.to_datetime(st.session_state["selected-start-date"])
end_date = pd.to_datetime(st.session_state["selected-end-date"])

# Diagrams
sleep_duration_over_time = health_diagrams.get_sleep_duration_over_time(user, start_date, end_date)
sleep_duration_per_time_blocks = health_diagrams.get_sleep_duration_per_time_blocks(user, start_date, end_date)
calories_burned_over_time = health_diagrams.get_calories_burned_over_time(user, start_date, end_date)
calories_burned_per_time_blocks = health_diagrams.get_calories_burned_per_time_blocks(user, start_date, end_date)
active_hrs_to_sleep_hrs = health_diagrams.get_active_hrs_to_sleep_hrs_regression(user, start_date, end_date)
sedentary_hrs_to_sleep_hrs = health_diagrams.get_sedentary_hrs_to_sleep_hrs_regression(user, start_date, end_date)
heart_rate_over_time, average_heart_rate = health_diagrams.get_heart_rate_over_time_and_average(user, start_date, end_date)

# Show on dashboard
st.plotly_chart(sleep_duration_over_time, key="sleep_duration_over_time")
st.plotly_chart(sleep_duration_per_time_blocks, key="sleep_duration_per_time_blocks")
st.plotly_chart(calories_burned_over_time, key="calories_burned_over_time")
st.plotly_chart(calories_burned_per_time_blocks, key="calories_burned_per_time_blocks")
st.plotly_chart(active_hrs_to_sleep_hrs, key="active_hrs_to_sleep_hrs")
st.plotly_chart(sedentary_hrs_to_sleep_hrs, key="sedentary_hrs_to_sleep_hrs")
st.plotly_chart(heart_rate_over_time, key="heart_rate_over_time")
st.plotly_chart(average_heart_rate, key="average_heart_rate")
