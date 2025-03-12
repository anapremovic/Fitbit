import streamlit as st
import pandas as pd

from scripts.dashboard.diagrams.health_diagrams import HealthDiagrams

health_diagrams = HealthDiagrams()
fig = health_diagrams.sleep_quantity_over_time(st.session_state["selected-user"],
                                               pd.to_datetime(st.session_state["selected-start-date"]),
                                               pd.to_datetime(st.session_state["selected-end-date"]))
st.pyplot(fig)

