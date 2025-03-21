# ----------
# Ensures that all Python files can be imported from any location
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
sys.path.append(project_root)
# ----------

import streamlit as st

from scripts.database import FitbitDatabase

@st.cache_resource
def get_fitbit_db_instance() -> FitbitDatabase:
    """Creates an instance of FitbitDatabase and, with that, establishes a connection
    to fitbit_database.db. The result should be saved to st.session_state so that 
    other pages can easily access this same instance.

    The decorator @st.cache_resource ensures the result is cached, so that this code is 
    only run once on startup.
    """

    db_location = os.path.join(project_root, "data/fitbit_database.db")
    return FitbitDatabase(db_location)

st.set_page_config(
    layout="wide",
)

fitbit_db = get_fitbit_db_instance()
st.session_state["fitbit-db"] = fitbit_db
st.session_state["project_root"] = project_root
st.session_state.setdefault("selected-user", "All")
st.session_state.setdefault("selected-start-date", fitbit_db.min_date)
st.session_state.setdefault("selected-end-date", fitbit_db.max_date)

home_page = st.Page("home_page.py", title="Home", icon="📌")
exercise_page = st.Page("exercise_page.py", title="Exercise", icon="🏋️")
health_page = st.Page("health_page.py", title="Health", icon="❤️")

pg = st.navigation([
    home_page, 
    exercise_page, 
    health_page
])

pg.run()

st.sidebar.header("Filters")

disable_filters = False
if st.session_state.get("current-page", "home") == "home":
    disable_filters = True

selected_user = st.sidebar.selectbox(
    "User ID",
    key="selected-user",
    options=("All",) + fitbit_db.user_ids,
    disabled=disable_filters,
)

left, right = st.sidebar.columns(2)
with left: 
    start_date = st.date_input(
        "Start date",
        key="selected-start-date",
        min_value=fitbit_db.min_date,
        max_value=st.session_state["selected-end-date"],
        disabled=disable_filters,
    )
with right:
    end_date = st.date_input(
        "End date",
        key="selected-end-date",
        min_value=st.session_state["selected-start-date"],
        max_value=fitbit_db.max_date,
        disabled=disable_filters,
    )
