import streamlit as st

from scripts.database import FitbitDatabase

fitbit_db: FitbitDatabase = st.session_state["fitbit_db"]
