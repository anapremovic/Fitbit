import streamlit as st
import pandas as pd

from scripts.dashboard.diagrams.health_diagrams import HealthDiagrams

health_diagrams = HealthDiagrams()
user = st.session_state["selected-user"]
start_date = pd.to_datetime(st.session_state["selected-start-date"])
end_date = pd.to_datetime(st.session_state["selected-end-date"])

sleep_quantity_over_time = health_diagrams.get_sleep_quantity_over_time(user, start_date, end_date)
st.pyplot(sleep_quantity_over_time)
