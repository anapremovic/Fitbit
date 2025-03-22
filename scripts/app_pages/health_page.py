import datetime as datetime
import streamlit as st
import pandas as pd

from scripts.diagrams.health_diagrams import HealthDiagrams

st.session_state["current-page"] = "health"

# Filters
user = st.session_state["selected-user"]
start_date = pd.to_datetime(st.session_state["selected-start-date"])
end_date = pd.to_datetime(st.session_state["selected-end-date"])

@st.cache_resource
def get_health_diagrams(user_id, start: datetime, end: datetime):
    return HealthDiagrams(st.session_state["fitbit-db"], user_id, start, end)
health_diagrams = get_health_diagrams(user, start_date, end_date)

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

st.markdown("""
            <style>
            .stSpinner > div {
                text-align: center;
                align-items: center;
                justify-content: center;
            }
            </style>
            """, unsafe_allow_html=True)
with st.spinner("Loading Data"):
    sleep_duration_over_time = health_diagrams.get_sleep_duration_over_time()
    sleep_duration_per_time_blocks = health_diagrams.get_sleep_duration_per_time_blocks()
    calories_burned_over_time = health_diagrams.get_calories_burned_over_time()
    calories_burned_per_time_blocks = health_diagrams.get_calories_burned_per_time_blocks()
    if st.session_state["weekdays-only"]:
        active_hrs_to_sleep_hrs = health_diagrams.get_active_hrs_to_sleep_hrs_regression("weekdays")
    elif st.session_state["weekends-only"]:
        active_hrs_to_sleep_hrs = health_diagrams.get_active_hrs_to_sleep_hrs_regression("weekends")
    else:
        active_hrs_to_sleep_hrs = health_diagrams.get_active_hrs_to_sleep_hrs_regression()
    sedentary_hrs_to_sleep_hrs = health_diagrams.get_sedentary_hrs_to_sleep_hrs_regression()
    heart_rate_over_time, average_heart_rate = health_diagrams.get_heart_rate_over_time_and_average()
    weight_over_time = health_diagrams.plot_weight_change_vs_steps()

# Show on dashboard

st.subheader("Sleep Duration")
with st.container(border=True):
    line, bar = st.columns(2)
    with line:
        st.plotly_chart(sleep_duration_over_time, key="sleep_duration_over_time")
    with bar:
        st.plotly_chart(sleep_duration_per_time_blocks, key="sleep_duration_per_time_blocks")

st.subheader("What Affects Sleep")
with st.container(border=True):
    weekdays, weekends = st.columns(2)
    with weekdays:
        st.toggle("Weekdays Only", key="weekdays-only", on_change=disable_weekends_toggle)
    with weekends:
        st.toggle("Weekends Only", key="weekends-only", on_change=disable_weekdays_toggle)
    st.plotly_chart(active_hrs_to_sleep_hrs, key="active_hrs_to_sleep_hrs")

with st.container(border=True):
    st.plotly_chart(sedentary_hrs_to_sleep_hrs, key="sedentary_hrs_to_sleep_hrs")

st.subheader("Calories")
with st.container(border=True):
    line, bar = st.columns(2)
    with line:
        st.plotly_chart(calories_burned_over_time, key="calories_burned_over_time")
    with bar:
        st.plotly_chart(calories_burned_per_time_blocks, key="calories_burned_per_time_blocks")

st.subheader("Heart Rate")
with st.container(border=True):
    plot, number = st.columns([3, 1])
    with plot:
        st.plotly_chart(heart_rate_over_time, key="heart_rate_over_time")
    with number:
        st.plotly_chart(average_heart_rate, key="average_heart_rate")

if weight_over_time:
    st.subheader("Weight")
    with st.container(border=True):
        st.plotly_chart(weight_over_time, key="weight_over_time")
