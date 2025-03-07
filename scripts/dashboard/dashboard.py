import streamlit as st
import os
import sys

# ----------
# Ensures that all Python files can be imported from any location

project_root = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
) 
sys.path.append(project_root)
# ----------
from scripts.database import FitbitDatabase as db
from scripts.dashboard import components as ct

db_location = os.path.join(project_root, "data/fitbit_database.db")
fitbit_database = db(db_location)

pages_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages")

home_page = st.Page(f"{pages_dir}/home.py", title="Home", icon="📌")
exercise_page = st.Page(f"{pages_dir}/exercise.py", title="Exercise", icon="🏋️")
health_page = st.Page(f"{pages_dir}/health.py", title="Health", icon="❤️")

pg = st.navigation([
    home_page, 
    exercise_page, 
    health_page
])

pg.run()
