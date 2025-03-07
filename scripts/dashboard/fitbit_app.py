# ----------
# Ensures that all Python files can be imported from any location
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
sys.path.append(project_root)
# ----------

import streamlit as st

from scripts.database import FitbitDatabase

home_page = st.Page("home_page.py", title="Home", icon="📌")
exercise_page = st.Page("exercise_page.py", title="Exercise", icon="🏋️")
health_page = st.Page("health_page.py", title="Health", icon="❤️")

pg = st.navigation([
    home_page, 
    exercise_page, 
    health_page
])

db_location = os.path.join(project_root, "data/fitbit_database.db")
fitbit_db = FitbitDatabase(db_location)

users = fitbit_db.get_all_user_ids()
users = tuple(users.loc[:, "Id"])
st.sidebar.selectbox(
    "User ID",
    ("All",) +  users,
    key = "selected_user"
)

pg.run()
