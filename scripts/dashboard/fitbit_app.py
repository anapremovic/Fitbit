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

st.session_state["fitbit_db"] = get_fitbit_db_instance()

@st.cache_data
def get_all_user_ids() -> tuple[str]:
    fitbit_db: FitbitDatabase = st.session_state["fitbit_db"]
    users = fitbit_db.get_all_user_ids()
    return tuple(users.loc[:, "Id"])

st.sidebar.selectbox(
        "User ID",
        ("All",) +  get_all_user_ids(),
        key = "selected_user"
    )

home_page = st.Page("home_page.py", title="Home", icon="📌")
exercise_page = st.Page("exercise_page.py", title="Exercise", icon="🏋️")
health_page = st.Page("health_page.py", title="Health", icon="❤️")

pg = st.navigation([
    home_page, 
    exercise_page, 
    health_page
])

pg.run()
