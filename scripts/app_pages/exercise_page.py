import datetime as datetime
import pandas as pd
import streamlit as st

from scripts.diagrams.exercise_diagrams import ExerciseDiagrams

user = st.session_state["selected-user"]
start_date = pd.to_datetime(st.session_state["selected-start-date"])
end_date = pd.to_datetime(st.session_state["selected-end-date"])

@st.cache_resource(show_spinner=False)
def get_exercise_diagrams(user_id, start: datetime, end: datetime):
    project_root = st.session_state["project-root"]
    return ExerciseDiagrams(st.session_state["fitbit-db"], f"{project_root}/data/chicago_data.csv",
                            user_id, start, end)
diagrams = get_exercise_diagrams(user, start_date, end_date)

st.subheader("Workouts")

with st.container(border=True):
    week, weather = st.columns(2)
    with week:
        st.plotly_chart(diagrams.get_day_of_week_frequency_graph())
    with weather:
        st.plotly_chart(diagrams.get_workout_frequency_by_weather_condition_graph())

st.subheader("Steps")

with st.container(border=True):
    heart_rate, calories, time_blocks = st.columns([2, 2, 1.5])
    with heart_rate:
        st.plotly_chart(diagrams.get_steps_to_heart_rate_regression())
    with calories:
        st.plotly_chart(diagrams.get_steps_to_calories_regression())
    with time_blocks:
        st.plotly_chart(diagrams.get_daily_steps_per_time_blocks_graph())

st.subheader("Temperature")

with st.container(border=True):
    calories, distance = st.columns(2)
    weather_figures = diagrams.get_weather_regressions()
    with distance:
        st.plotly_chart(weather_figures["calories_vs_temp"])
    with calories:
        st.plotly_chart(weather_figures["distance_vs_temp"])
