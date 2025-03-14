import datetime as datetime
import plotly.express as px
import plotly.graph_objects as go

from scripts.database import FitbitDatabase

class HealthDiagrams:
    def __init__(self, fitbit_db: FitbitDatabase):
        self.fitbit_db = fitbit_db

    def get_sleep_duration_over_time(self, user_id, first_date: datetime, last_date: datetime) -> go.Figure():
        """Returns a Plotly figure that visualizes the number of hours slept each day."""
        sleep_moments = self.fitbit_db.get_sleep_moments()

        # Filter Dates
        sleep_moments = sleep_moments[(sleep_moments["Date"] >= first_date) & (sleep_moments["Date"] <= last_date)]

        # Filter UserIds
        if user_id == "All":
            sleep_moments = sleep_moments.groupby("Date", as_index=False)["SleepHours"].mean() # Change to average sleep hours
            title = "Sleep Duration Over Time For All Users"
            y_label = "Average Hours Slept"
        else:
            sleep_moments = sleep_moments[sleep_moments.loc[:, "UserId"] == user_id] # Filter by user
            title = f"Sleep Duration Over Time For User {user_id}"
            y_label = "Hours Slept"

        if sleep_moments.empty:
            return go.Figure()

        return px.line(sleep_moments, x="Date", y="SleepHours", title=title, labels=dict(SleepHours=y_label))
