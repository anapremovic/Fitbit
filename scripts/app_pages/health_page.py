import datetime as datetime
import streamlit as st
import pandas as pd

from scripts.diagrams.health_diagrams import HealthDiagrams

st.session_state["current-page"] = "health"

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

st.subheader("Sleep Duration")
with st.container(border=True):
    line, bar = st.columns(2)
    with line:
        st.plotly_chart(diagrams.get_sleep_duration_over_time_graph())
    with bar:
        st.plotly_chart(diagrams.get_sleep_duration_per_time_blocks_graph())

st.subheader("What Affects Sleep")
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

with st.container(border=True):
    st.plotly_chart(diagrams.get_sedentary_hrs_to_sleep_hrs_regression())

st.subheader("Calories")
with st.container(border=True):
    line, bar = st.columns(2)
    with line:
        st.plotly_chart(diagrams.get_calories_burned_over_time_graph())
    with bar:
        st.plotly_chart(diagrams.get_calories_burned_per_time_blocks_graph())

st.subheader("Heart Rate")
heart_rate_over_time, average_heart_rate = diagrams.get_heart_rate_over_time_and_average_graphs()
with st.container(border=True):
    plot, number = st.columns([3, 1])
    with plot:
        st.plotly_chart(heart_rate_over_time)
    with number:
        st.plotly_chart(average_heart_rate)

weight_over_time = diagrams.get_weight_change_to_steps_regression()
if weight_over_time:
    st.subheader("Weight")
    with st.container(border=True):
        st.plotly_chart(weight_over_time)
