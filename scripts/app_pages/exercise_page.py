import datetime as datetime
import pandas as pd
import streamlit as st

from scripts.diagrams.exercise_diagrams import ExerciseDiagrams

st.session_state["current-page"] = "exercise"

user = st.session_state["selected-user"]
start_date = pd.to_datetime(st.session_state["selected-start-date"])
end_date = pd.to_datetime(st.session_state["selected-end-date"])

@st.cache_resource
def get_exercise_diagrams(user_id, start: datetime, end: datetime):
    project_root = st.session_state["project-root"]
    return ExerciseDiagrams(st.session_state["fitbit-db"], f"{project_root}/data/chicago_data.csv",
                            user_id, start, end)
# If you see this in the PR it means i forgot to change it back so leave a comment
project_root = st.session_state["project-root"]
diagrams = ExerciseDiagrams(st.session_state["fitbit-db"], f"{project_root}/data/chicago_data.csv",
                            user, start_date, end_date)

daily, hourly, scatter = st.columns([1, 1, 2])
with daily:
    st.plotly_chart(diagrams.get_day_of_week_frequency_graph())
with hourly:
    st.plotly_chart(diagrams.get_daily_steps_per_time_blocks_graph())
with scatter:
    st.plotly_chart(diagrams.get_steps_to_calories_regression())

weather_figures = diagrams.get_weather_regressions()
conditions, calories, distance = st.columns([1, 1.5, 1.5])
with conditions:
    st.plotly_chart(diagrams.get_workout_frequency_by_weather_condition_graph())
with distance:
    st.plotly_chart(weather_figures["distance_vs_temp"])
with calories:
    st.plotly_chart(weather_figures["calories_vs_temp"])

steps_to_heart_rate, avg_heart_rate_diagram = diagrams.get_steps_to_heart_rate_and_avg_heart_rate_graphs()
graph, numerical = st.columns([4, 1])
with graph:
    st.plotly_chart(steps_to_heart_rate)
with numerical:
    st.plotly_chart(avg_heart_rate_diagram)
