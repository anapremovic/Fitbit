import streamlit as st

from scripts.dashboard.diagrams.health_diagrams import HealthDiagrams

health_diagrams = HealthDiagrams()
fig = health_diagrams.sleep_quantity_over_time(st.session_state["selected_user"])
st.pyplot(fig)

