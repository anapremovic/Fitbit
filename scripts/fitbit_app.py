# ----------
# Ensures that all Python files can be imported from any location
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
# ----------

import streamlit as st

from database import FitbitDatabase

@st.cache_resource
def get_fitbit_db_instance() -> FitbitDatabase:
    """Creates an instance of FitbitDatabase and establishes a connection
    to fitbit_database.db. The result should be saved to st.session_state so that
    all pages can easily access this same instance.

    The decorator @st.cache_resource ensures the result is cached, so that this code is 
    only run once on startup.
    """

    db_location = os.path.join(project_root, "data/fitbit_database.db")
    return FitbitDatabase(db_location)

st.set_page_config(
    layout="wide",
)

home_page = st.Page("app_pages/home_page.py", title="Home", icon="📌")
exercise_page = st.Page("app_pages/exercise_page.py", title="Exercise", icon="🏋️")
health_page = st.Page("app_pages/health_page.py", title="Health", icon="❤️")

pg = st.navigation([
    home_page, 
    exercise_page, 
    health_page
], position="hidden")

fitbit_db = get_fitbit_db_instance()
st.session_state["fitbit-db"] = fitbit_db
st.session_state["project-root"] = project_root
st.session_state.setdefault("selected-user", "All")
st.session_state.setdefault("selected-start-date", fitbit_db.min_date)
st.session_state.setdefault("selected-end-date", fitbit_db.max_date)
st.session_state.setdefault("current-page", "home")
# if "current-page" not in st.session_state:
#     st.session_state["current-page"] = "home"

def switch_page(page: str):
    st.session_state["change-page"] = True
    st.session_state["current-page"] = page

pad1, home, pad2, exercise, pad3, health, pad4 = st.columns([1, 2, 1, 2, 1, 2, 1], vertical_alignment='center')
pad1.divider()
home.button(
    "Home", 
    on_click=switch_page,
    args=["home"],
    type="primary" if st.session_state["current-page"] == "home" else "secondary",
    use_container_width=True,
)
pad2.divider()
exercise.button(
    "Exercise",
    on_click=switch_page,
    args=["exercise"],
    type="primary" if st.session_state["current-page"] == "exercise" else "secondary",
    use_container_width=True,
)
pad3.divider()
health.button(
    "Health", 
    on_click=switch_page,
    args=["health"],
    type="primary" if st.session_state["current-page"] == "health" else "secondary",
    use_container_width=True,
)
pad4.divider()

if st.session_state.get("change-page"):
    st.session_state["change-page"] = False
    match st.session_state["current-page"]:
        case "home":
            st.switch_page(home_page)
        case "exercise":
            st.switch_page(exercise_page)
        case "health":
            st.switch_page(health_page)

are_filters_disabled = st.session_state["current-page"] == "home"
start_filter, user_filter, end_filter = st.columns(3)
user_filter.selectbox(
    "User ID",
    key="selected-user",
    options=("All",) + fitbit_db.user_ids,
    disabled=are_filters_disabled,
)
start_filter.date_input(
    "Start date",
    key="selected-start-date",
    min_value=fitbit_db.min_date,
    max_value=st.session_state["selected-end-date"],
    disabled=are_filters_disabled,
)
end_filter.date_input(
    "End date",
    key="selected-end-date",
    min_value=st.session_state["selected-start-date"],
    max_value=fitbit_db.max_date,
    disabled=are_filters_disabled,
)

pg.run()
