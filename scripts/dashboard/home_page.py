import streamlit as st

from scripts.database import FitbitDatabase
from scripts.dashboard.diagrams.home_diagrams import HomeDiagrams

@st.cache_resource
def get_home_diagrams():
    return HomeDiagrams(st.session_state["fitbit_db"])
home_diagrams = get_home_diagrams()
