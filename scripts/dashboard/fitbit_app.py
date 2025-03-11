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

fitbit_db = get_fitbit_db_instance()
st.session_state["fitbit_db"] = fitbit_db
st.session_state["selected_user"] = None

st.sidebar.header("Filters")

def update_selected_user():
    if st.session_state["selected_user"] == "All":
        st.session_state["selected_user"] = None

selected_user = st.sidebar.selectbox(
    "User ID",
    key="selected_user",
    options=("All",) + fitbit_db.user_ids,
    on_change=update_selected_user
)


# Un-comment this to see the corresponding user's id on the dashboard
# if selected_user:
#     st.write(selected_user)

left, right = st.sidebar.columns(2)
with left: 
    start_date = st.date_input(
        "Start date", 
        key="selected-start-date", 
        value=fitbit_db.chosen_start, 
        min_value=fitbit_db.first_date, 
        max_value=fitbit_db.chosen_end,
    )
with right:
    end_date = st.date_input(
        "End date", 
        key="selected-end-date", 
        value=fitbit_db.chosen_end, 
        min_value=fitbit_db.chosen_start, 
        max_value=fitbit_db.last_date
    )

fitbit_db.chosen_start = start_date
fitbit_db.chosen_end = end_date

sleep_moments = fitbit_db.get_sleep_moments(st.session_state["selected_user"])
print(sleep_moments)
st.write(sleep_moments)

home_page = st.Page("home_page.py", title="Home", icon="📌")
exercise_page = st.Page("exercise_page.py", title="Exercise", icon="🏋️")
health_page = st.Page("health_page.py", title="Health", icon="❤️")

pg = st.navigation([
    home_page, 
    exercise_page, 
    health_page
])

pg.run()
