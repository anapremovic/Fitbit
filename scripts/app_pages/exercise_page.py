import datetime as datetime
import streamlit as st
import pandas as pd

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
diagrams = get_exercise_diagrams(user, start_date, end_date)

st.title("Exercise")

density, bar = st.columns(2)
with density:
    st.plotly_chart(diagrams.plot_distance_walked_density())
with bar:
    st.plotly_chart(diagrams.plot_day_of_week_frequency())

st.plotly_chart(diagrams.plot_steps_to_calories_regression())

st.subheader("Correlations Between Distance, Calories, Temperature, and Precipitation")

weather_figures = diagrams.plot_weather_correlation_for_chicago()
temp, precip = st.columns(2)
with temp:
    st.plotly_chart(weather_figures["distance_vs_temp"])
    st.plotly_chart(weather_figures["calories_vs_temp"])
with precip:
    st.plotly_chart(weather_figures["distance_vs_precip"])
    st.plotly_chart(weather_figures["calories_vs_precip"])

st.subheader("Daily Distributions")

st.plotly_chart(diagrams.plot_daily_step_distribution_barplot())

steps_to_heart_rate, avg_heart_rate_diagram = diagrams.plot_steps_to_heart_rate_and_avg_heart_rate()
graph, numerical = st.columns([4, 1])
with graph:
    st.plotly_chart(steps_to_heart_rate)
with numerical:
    st.plotly_chart(avg_heart_rate_diagram)
