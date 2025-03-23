import datetime as datetime
import pandas as pd
import streamlit as st

from scripts.diagrams.health_diagrams import HealthDiagrams

user = st.session_state["selected-user"]
start_date = pd.to_datetime(st.session_state["selected-start-date"])
end_date = pd.to_datetime(st.session_state["selected-end-date"])

@st.cache_resource
def get_health_diagrams(user_id, start: datetime, end: datetime):
    return HealthDiagrams(st.session_state["fitbit-db"], user_id, start, end)
diagrams = get_health_diagrams(user, start_date, end_date)

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

st.subheader("Sleep")

with st.container(border=True):
    line, bar, scatter = st.columns([1, 1, 2])
    with line:
        st.plotly_chart(diagrams.get_sleep_duration_over_time_graph())
    with bar:
        st.plotly_chart(diagrams.get_sleep_duration_per_time_blocks_graph())
    with scatter:
        st.plotly_chart(diagrams.get_sedentary_hrs_to_sleep_hrs_regression())

with st.container(border=True):
    weekdays, weekends = st.columns(2)
    with weekdays:
        st.toggle("Weekdays Only", key="weekdays-only", on_change=disable_weekends_toggle)
    with weekends:
        st.toggle("Weekends Only", key="weekends-only", on_change=disable_weekdays_toggle)

    if st.session_state["weekdays-only"]:
        st.plotly_chart(diagrams.get_active_hrs_to_sleep_hrs_regression("weekdays"))
    elif st.session_state["weekends-only"]:
        st.plotly_chart(diagrams.get_active_hrs_to_sleep_hrs_regression("weekends"))
    else:
        st.plotly_chart(diagrams.get_active_hrs_to_sleep_hrs_regression())

st.subheader("Heart Rate And Calories")

with st.container(border=True):
    calories_line, calories_bar, heart_rate_line, heart_rate_indicator = st.columns([2, 2, 3, 1])

    with calories_line:
        st.plotly_chart(diagrams.get_calories_burned_over_time_graph())
    with calories_bar:
        st.plotly_chart(diagrams.get_calories_burned_per_time_blocks_graph())

    heart_rate_over_time, average_heart_rate = diagrams.get_heart_rate_over_time_and_average_graphs()
    with heart_rate_line:
        st.plotly_chart(heart_rate_over_time)
    with heart_rate_indicator:
        st.plotly_chart(average_heart_rate)

st.subheader("Weight")
with st.container(border=True):
    st.plotly_chart(diagrams.get_weight_and_steps_over_time_graphs())
