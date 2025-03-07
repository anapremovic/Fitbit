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

db_location = os.path.join(project_root, "data/fitbit_database.db")
fitbit_database = FitbitDatabase(db_location)

st.header("Home")
st.sidebar.header("Home")
