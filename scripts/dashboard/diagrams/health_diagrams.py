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

        return px.line(sleep_moments, x="Date", y="SleepHours", title=title, labels=dict(SleepHours=y_label))

    def get_sedentary_hrs_to_sleep_hrs_regression(self, user_id, start_date: datetime, end_date: datetime) -> go.Figure():
        """Returns a Plotly figure of a regression between hours spent sedentary and hours slept."""
        sedentary_and_sleep_data = self.fitbit_db.get_sedentary_sleep_activity()

        sedentary_and_sleep_data = self._filter_dates(sedentary_and_sleep_data, start_date, end_date)
        title = "Relation Between Daily Sedentary Time And Sleep Duration For All Users"
        if user_id != "All":
            title = f"Relation Between Daily Sedentary Time and Sleep Duration For User {user_id}"
            sedentary_and_sleep_data = self._filter_users(sedentary_and_sleep_data, user_id)

        return px.scatter(sedentary_and_sleep_data, x="SedentaryHours", y="HoursSlept", trendline="ols",
                          title=title, labels=dict(SedentaryHours="Sedentary Hours", HoursSlept="Hours Slept"))

    def get_active_hrs_to_sleep_hrs_regression(self, user_id, start_date: datetime, end_date: datetime) -> go.Figure():
        """Returns a Plotly figure of a regression between hours spent active and hours slept"""
        active_and_sleep_data = self.fitbit_db.get_active_and_sleep_hrs("")

        active_and_sleep_data = self._filter_dates(active_and_sleep_data, start_date, end_date)
        title = "Relation Between Daily Active Time And Sleep Duration For All Users"
        if user_id != "All":
            title = f"Relation Between Daily Active Time And Sleep Duration For User {user_id}"
            active_and_sleep_data = self._filter_users(active_and_sleep_data, user_id)

        return px.scatter(active_and_sleep_data, x="TotalActiveHours", y="TotalSleepHours", trendline="ols",
                          title=title, labels=dict(TotalActiveHours="Active Hours", TotalSleepHours="Hours Slept"))

    def get_sleep_duration_per_time_blocks(self, user_id, start_date: datetime, end_date: datetime) -> go.Figure():
        """Returns a Plotly figure of a bar plot that divides a day into 6 4-hour time blocks and computes the average
        sleep duration per time block."""
        sleep_data = self.fitbit_db.get_daily_sleep_distribution()

        sleep_data = self._filter_dates(sleep_data, start_date, end_date)

        sleep_data = sleep_data.groupby((["UserId", "HourGroup"]), as_index=False, observed=False)["TotalHoursSlept"].mean()
        sleep_data.rename(columns={"TotalHoursSlept": "AverageHoursSlept"}, inplace=True) # Average for time block

        if user_id == "All":
            sleep_data = sleep_data.groupby("HourGroup", as_index=False, observed=False)["AverageHoursSlept"].mean() # Average over all users
            title = "Sleep Duration Per 4-Hour Time Blocks For All Users"
        else:
            sleep_data = self._filter_users(sleep_data, user_id)
            title = f"Sleep Duration Per 4-Hour Time Blocks For User {user_id}"

        return px.bar(sleep_data, x="HourGroup", y="AverageHoursSlept", title=title,
                      labels=dict(HourGroup="Time", AverageHoursSlept="Average Hours Slept"))

    def get_heart_rate_over_time_and_average(self, user_id, start_date: datetime, end_date: datetime) -> (go.Figure(), go.Figure()):
        """Returns a Plotly figure that visualizes the heart rate each day."""
        heart_rate_data = self.fitbit_db.get_heart_rate()

        heart_rate_data = self._filter_dates(heart_rate_data, start_date, end_date)
        if user_id == "All":
            heart_rate_data = heart_rate_data.groupby("Date", as_index=False)["HeartRate"].mean()
            over_time_plot_title = "Heart Rate Over Time For All Users"
            over_time_plot_y_label = "Average Heart Rate (bpm)"
            average_plot_title = "Average Heart Rate For All Users Over Date Range"
        else:
            heart_rate_data = self._filter_users(heart_rate_data, user_id)
            over_time_plot_title = f"Heart Rate Over Time For User {user_id}"
            over_time_plot_y_label = "Heart Rate (bpm)"
            average_plot_title = f"Average Heart Rate For User {user_id} Over Date Range"

        avg_heart_rate = heart_rate_data.loc[:, "HeartRate"].mean()

        over_time_plot = px.line(heart_rate_data, x="Date", y="HeartRate", title=over_time_plot_title, labels=dict(HeartRate=over_time_plot_y_label))
        average_plot = go.Figure(go.Scatter(
            x=[0],
            y=[0],
            text=[avg_heart_rate],
            mode='text',
            textfont=dict(size=50),
        ))
        average_plot.update_layout(
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            title=average_plot_title,
            title_y=0.95
        )

        return over_time_plot, average_plot
