import streamlit as st
import os
import sys

# ----------
# Ensures that all Python files can be imported from any location

project_root = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
				os.path.abspath(__file__)
            )
        )
    )
) 
sys.path.append(project_root)
# ----------

# Imports must go after setting up project root
from scripts.database import FitbitDatabase
from scripts.dashboard import components as ct

db_location = os.path.join(project_root, "data/fitbit_database.db")
fitbit_database = FitbitDatabase(db_location)

st.header("Home")
st.sidebar.header("Home")

dashboard = ct.DashboardComponents(fitbit_database)
selected_user = dashboard.user_id_sidebar()


# Display selected user
if selected_user:
    st.write(f"### Selected User: {selected_user}")