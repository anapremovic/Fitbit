import datetime as datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from scripts.database import FitbitDatabase

class HealthDiagrams:
    def __init__(self, fitbit_db: FitbitDatabase):
        self.fitbit_db = fitbit_db

    def _filter_dates(self, df: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Helper function to filter DataFrame by user selected date range from dashboard."""
        return df[(df.loc[:, "Date"] >= start_date) & (df.loc[:, "Date"] <= end_date)]

    def _filter_users(self, df: pd.DataFrame, user_id: float):
        """Helper function to filter DataFrame by user selected user ID from dashboard."""
        return df[(df.loc[:, "UserId"] == user_id)]

    def get_sleep_duration_over_time(self, user_id, start_date: datetime, end_date: datetime) -> go.Figure():
        """Returns a Plotly figure that visualizes the number of hours slept each day."""
        sleep_moments = self.fitbit_db.get_sleep_moments()

        sleep_moments = self._filter_dates(sleep_moments, start_date, end_date)
        if user_id == "All":
            sleep_moments = sleep_moments.groupby("Date", as_index=False)["SleepHours"].mean() # Change to average sleep hours
            title = "Sleep Duration Over Time For All Users"
            y_label = "Average Hours Slept"
        else:
            sleep_moments = self._filter_users(sleep_moments, user_id)
            title = f"Sleep Duration Over Time For User {user_id}"
            y_label = "Hours Slept"

        if sleep_moments.empty:
            return go.Figure()

        return px.line(sleep_moments, x="Date", y="SleepHours", title=title, labels=dict(SleepHours=y_label))

    def get_sedentary_hrs_to_sleep_hrs_regression(self, user_id, start_date: datetime, end_date: datetime) -> go.Figure():
        """Returns a Plotly figure of a regression between minutes spent sedentary and minutes slept."""
        sedentary_and_sleep_data = self.fitbit_db.get_sedentary_sleep_activity()

        sedentary_and_sleep_data = self._filter_dates(sedentary_and_sleep_data, start_date, end_date)
        title = "Relation Between Daily Sedentary Time and Sleep Duration For All Users"
        if user_id != "All":
            title = F"Relation Between Daily Sedentary Time and Sleep Duration For User {user_id}"
            sedentary_and_sleep_data = self._filter_users(sedentary_and_sleep_data, user_id)

        if sedentary_and_sleep_data.empty:
            return go.Figure()

        return px.scatter(sedentary_and_sleep_data, x="SedentaryHours", y="HoursSlept", trendline="ols",
                          title=title, labels=dict(SedentaryHours="Sedentary Hours", HoursSlept="Hours Slept"))
