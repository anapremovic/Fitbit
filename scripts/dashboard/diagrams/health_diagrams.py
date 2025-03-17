import datetime as datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from scripts.database import FitbitDatabase

class HealthDiagrams:
    def __init__(self, fitbit_db: FitbitDatabase):
        self.fitbit_db = fitbit_db

    @staticmethod # Not bound to a specific instance of HealthDiagrams, just a helper
    def filter_by_date_range(df: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Helper function to filter DataFrame by user selected date range from dashboard."""
        return df[(df.loc[:, "Date"] >= start_date) & (df.loc[:, "Date"] <= end_date)]

    @staticmethod # Not bound to a specific instance of HealthDiagrams, just a helper
    def filter_by_user(df: pd.DataFrame, user_id: float) -> pd.DataFrame:
        """Helper function to filter DataFrame by user selected user ID from dashboard."""
        return df[(df.loc[:, "UserId"] == user_id)]

    def get_sleep_duration_over_time(self, user_id, start_date: datetime, end_date: datetime) -> go.Figure:
        """Returns a Plotly figure that visualizes the number of hours slept each day."""
        sleep_moments = self.fitbit_db.get_sleep_moments()

        sleep_moments = HealthDiagrams.filter_by_date_range(sleep_moments, start_date, end_date)
        if user_id == "All":
            sleep_moments = sleep_moments.groupby("Date", as_index=False)["SleepHours"].mean() # Average over all users
            title = "Sleep Duration Over Time For All Users"
            y_label = "Average Hours Slept"
        else:
            sleep_moments = HealthDiagrams.filter_by_user(sleep_moments, user_id)
            title = f"Sleep Duration Over Time For User {user_id}"
            y_label = "Hours Slept"

        return px.line(sleep_moments, x="Date", y="SleepHours", title=title, labels=dict(SleepHours=y_label))

    def get_sedentary_hrs_to_sleep_hrs_regression(self, user_id, start_date: datetime, end_date: datetime) -> go.Figure:
        """Returns a Plotly figure of a regression between hours spent sedentary and hours slept."""
        sedentary_and_sleep_data = self.fitbit_db.get_sedentary_sleep_activity()

        sedentary_and_sleep_data = HealthDiagrams.filter_by_date_range(sedentary_and_sleep_data, start_date, end_date)
        title = "Relation Between Daily Sedentary Time And Sleep Duration For All Users"
        if user_id != "All":
            title = f"Relation Between Daily Sedentary Time and Sleep Duration For User {user_id}"
            sedentary_and_sleep_data = HealthDiagrams.filter_by_user(sedentary_and_sleep_data, user_id)

        return px.scatter(sedentary_and_sleep_data, x="SedentaryHours", y="HoursSlept", trendline="ols", title=title,
                          labels=dict(SedentaryHours="Sedentary Hours", HoursSlept="Hours Slept"), opacity=0.5)

    def get_active_hrs_to_sleep_hrs_regression(self, user_id, start_date: datetime, end_date: datetime, week_period: str = "") -> go.Figure:
        """Returns a Plotly figure of a regression between hours spent active and hours slept"""
        active_and_sleep_data = self.fitbit_db.get_active_and_sleep_hrs(week_period)

        active_and_sleep_data = HealthDiagrams.filter_by_date_range(active_and_sleep_data, start_date, end_date)
        title = "Relation Between Daily Active Time And Sleep Duration For All Users"
        if user_id != "All":
            title = f"Relation Between Daily Active Time And Sleep Duration For User {user_id}"
            active_and_sleep_data = HealthDiagrams.filter_by_user(active_and_sleep_data, user_id)

        return px.scatter(active_and_sleep_data, x="TotalActiveHours", y="TotalSleepHours", trendline="ols", title=title,
                          labels=dict(TotalActiveHours="Active Hours", TotalSleepHours="Hours Slept"), opacity=0.5)

    def get_sleep_duration_per_time_blocks(self, user_id, start_date: datetime, end_date: datetime) -> go.Figure:
        """Returns a Plotly figure of a bar plot that divides a day into 6 4-hour time blocks and computes the average
        sleep duration per time block."""
        sleep_data = self.fitbit_db.get_daily_sleep_distribution()

        sleep_data = HealthDiagrams.filter_by_date_range(sleep_data, start_date, end_date)
        title = "Average Sleep Duration Per 4-Hour Time Blocks For All Users"
        if user_id != "All":
            sleep_data = HealthDiagrams.filter_by_user(sleep_data, user_id)
            title = f"Average Sleep Duration Per 4-Hour Time Blocks For User {user_id}"
        sleep_data = sleep_data.groupby("HourGroup", as_index=False, observed=False)["HoursSlept"].mean() # Average over all dates

        return px.bar(sleep_data, x="HourGroup", y="HoursSlept", title=title,
                      labels=dict(HourGroup="Time", HoursSlept="Average Hours Slept"))

    def get_calories_burned_over_time(self, user_id, start_date: datetime, end_date: datetime) -> go.Figure:
        """Returns a Plotly figure that visualizes the number of calories burned each day."""
        calorie_data = self.fitbit_db.get_calories()

        calorie_data = HealthDiagrams.filter_by_date_range(calorie_data, start_date, end_date)
        if user_id == "All":
            calorie_data = calorie_data.groupby("Date", as_index=False)["Calories"].mean() # Average over all users
            title = "Calories Burned Over Time For All Users"
            y_label = "Average Calories Burned"
        else:
            calorie_data = HealthDiagrams.filter_by_user(calorie_data, user_id)
            title = f"Calories Burned Over Time For User {user_id}"
            y_label = "Calories Burned"

        return px.line(calorie_data, x="Date", y="Calories", title=title, labels=dict(Calories=y_label))

    def get_calories_burned_per_time_blocks(self, user_id, start_date: datetime, end_date: datetime) -> go.Figure:
        """Returns a Plotly figure of a bar plot that divides a day into 6 4-hour time blocks and computes the average
        calories burned per time block."""
        calorie_data = self.fitbit_db.get_daily_calorie_distribution()

        calorie_data = HealthDiagrams.filter_by_date_range(calorie_data, start_date, end_date)
        title = "Calories Burned Per 4-Hour Time Blocks For All Users"
        if user_id != "All":
            calorie_data = HealthDiagrams.filter_by_user(calorie_data, user_id)
            title = f"Calories Burned Per 4-Hour Time Blocks For User {user_id}"
        calorie_data = calorie_data.groupby("HourGroup", as_index=False, observed=False)["AverageCalories"].mean()  # Average over all dates

        return px.bar(calorie_data, x="HourGroup", y="AverageCalories", title=title,
                      labels=dict(HourGroup="Time", AverageCalories="Average Calories Burned"))

    def get_heart_rate_over_time_and_average(self, user_id, start_date: datetime, end_date: datetime) -> (go.Figure, go.Figure):
        """Returns a Plotly figure that visualizes the heart rate each day."""
        heart_rate_data = self.fitbit_db.get_heart_rate()

        heart_rate_data = HealthDiagrams.filter_by_date_range(heart_rate_data, start_date, end_date)
        if user_id == "All":
            heart_rate_data = heart_rate_data.groupby("Date", as_index=False)["HeartRate"].mean() # Average over all users
            over_time_plot_title = "Heart Rate Over Time For All Users"
            over_time_plot_y_label = "Average Heart Rate (bpm)"
            average_plot_title = "Average Heart Rate" + "<br>" + "For All Users" + "<br>" + "Over Date Range"
        else:
            heart_rate_data = HealthDiagrams.filter_by_user(heart_rate_data, user_id)
            over_time_plot_title = f"Heart Rate Over Time For User {user_id}"
            over_time_plot_y_label = "Heart Rate (bpm)"
            average_plot_title = "Average Heart Rate" + "<br>" + f"For User {user_id}" + "<br>" + "Over Date Range"

        if heart_rate_data.empty:
            avg_heart_rate = "No Data"
        else:
            avg_heart_rate = "{0:.2f}".format(heart_rate_data.loc[:, "HeartRate"].mean()) # Average over all dates

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
