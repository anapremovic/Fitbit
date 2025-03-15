import streamlit as st
import pandas as pd

from scripts.dashboard.diagrams.health_diagrams import HealthDiagrams

# Filters
health_diagrams = HealthDiagrams(st.session_state["fitbit_db"])
user = st.session_state["selected-user"]
start_date = pd.to_datetime(st.session_state["selected-start-date"])
end_date = pd.to_datetime(st.session_state["selected-end-date"])

# Toggles
if "weekdays-only" not in st.session_state:
    st.session_state["weekdays-only"] = False
if "weekends-only" not in st.session_state:
    st.session_state["weekends-only"] = False
def disable_weekends_toggle():
    if st.session_state["weekdays-only"]:
        st.session_state["weekends-only"] = False
def disable_weekdays_toggle():
    if st.session_state["weekends-only"]:
        st.session_state["weekdays-only"] = False

# Diagrams
sleep_duration_over_time = health_diagrams.get_sleep_duration_over_time(user, start_date, end_date)
sleep_duration_per_time_blocks = health_diagrams.get_sleep_duration_per_time_blocks(user, start_date, end_date)
calories_burned_over_time = health_diagrams.get_calories_burned_over_time(user, start_date, end_date)
calories_burned_per_time_blocks = health_diagrams.get_calories_burned_per_time_blocks(user, start_date, end_date)
if st.session_state["weekdays-only"]:
    active_hrs_to_sleep_hrs = health_diagrams.get_active_hrs_to_sleep_hrs_regression(user, start_date, end_date, "weekdays")
elif st.session_state["weekends-only"]:
    active_hrs_to_sleep_hrs = health_diagrams.get_active_hrs_to_sleep_hrs_regression(user, start_date, end_date, "weekends")
else:
    active_hrs_to_sleep_hrs = health_diagrams.get_active_hrs_to_sleep_hrs_regression(user, start_date, end_date)
sedentary_hrs_to_sleep_hrs = health_diagrams.get_sedentary_hrs_to_sleep_hrs_regression(user, start_date, end_date)
heart_rate_over_time, average_heart_rate = health_diagrams.get_heart_rate_over_time_and_average(user, start_date, end_date)

# Show on dashboard

# Sleep
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(sleep_duration_over_time, key="sleep_duration_over_time")
with col2:
    st.plotly_chart(sleep_duration_per_time_blocks, key="sleep_duration_per_time_blocks")

col1, col2 = st.columns(2)
with col1:
    st.toggle("Weekdays Only", key="weekdays-only", on_change=disable_weekends_toggle)
with col2:
    st.toggle("Weekends Only", key="weekends-only", on_change=disable_weekdays_toggle)
st.plotly_chart(active_hrs_to_sleep_hrs, key="active_hrs_to_sleep_hrs")

st.plotly_chart(sedentary_hrs_to_sleep_hrs, key="sedentary_hrs_to_sleep_hrs")

# Calories
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(calories_burned_over_time, key="calories_burned_over_time")
with col2:
    st.plotly_chart(calories_burned_per_time_blocks, key="calories_burned_per_time_blocks")

# Heart Rate
col1, col2 = st.columns([3, 1])
with col1:
    st.plotly_chart(heart_rate_over_time, key="heart_rate_over_time")
with col2:
    st.plotly_chart(average_heart_rate, key="average_heart_rate")
