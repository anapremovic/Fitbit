import datetime as datetime
import streamlit as st
import pandas as pd

from scripts.dashboard.diagrams.exercise_diagrams import ExerciseDiagrams

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
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(diagrams.plot_distance_walked_density())
st.plotly_chart(diagrams.plot_steps_to_calories_regression())

with col2:
    st.plotly_chart(diagrams.plot_day_of_week_frequency())

chicago_figures = diagrams.plot_weather_correlation_for_chicago()

st.subheader("Correlations Between Distance, Calories, Temperature, and Precipitation")
temp, precip = st.columns(2)

with temp:
    st.plotly_chart(chicago_figures["distance_vs_temp"])
    st.plotly_chart(chicago_figures["calories_vs_temp"])

with precip:
    st.plotly_chart(chicago_figures["distance_vs_precip"])
    st.plotly_chart(chicago_figures["calories_vs_precip"])

st.subheader("Daily Distributions")
st.plotly_chart(diagrams.plot_daily_step_distribution_barplot())

heart_rate_graph, avg_heart_rate = st.columns([4, 1])

heart_rate_graph_diagram, avg_heart_rate_diagram = diagrams.plot_steps_to_heart_rate_and_avg_heart_rate()

with heart_rate_graph: st.plotly_chart(heart_rate_graph_diagram)
with avg_heart_rate: st.plotly_chart(avg_heart_rate_diagram)
