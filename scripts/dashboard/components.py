import streamlit as st
from scripts.database import FitbitDatabase
import pandas as pd

class DashboardComponents:
	"""
	Purpose: Parts of our dashboard that are repeated
	"""
	def __init__(self, db: FitbitDatabase):
		self.db = db

	def user_id_sidebar(self):
		df_ids = self.db.get_unique_user_ids()

		selected_user = st.sidebar.selectbox(
			"Select a user:",
			df_ids.to_numpy().flatten()  # Convert to a 1D array
		)

		return selected_user  # Return the selected user
