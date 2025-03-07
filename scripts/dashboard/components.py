import streamlit as st
from ...scripts import database as db
import os
import sys

# project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# file_location = os.path.join(project_root, "database.py") # CHANGE LATER
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
sys.path.append(project_root)

def user_id_sidebar():
	print(db.get_unique_user_ids())
	# return st.sidebar.selectbox("Users", options=["a", "b"])
