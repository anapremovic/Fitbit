import datetime as datetime
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from scripts.utils.util import Util
from scripts.database import FitbitDatabase

class HealthDiagrams:
    def __init__(self, fitbit_db: FitbitDatabase, user, start_date: datetime, end_date: datetime):
        self.fitbit_db = fitbit_db
        self.user = user
        self.start_date = start_date
        self.end_date = end_date

    def get_sleep_duration_over_time(self) -> go.Figure:
        """Returns a Plotly figure that visualizes the number of hours slept each day."""
        sleep_moments = self.fitbit_db.get_sleep_moments()

        sleep_moments = Util.filter_by_date_range(sleep_moments, self.start_date, self.end_date)
        if self.user == "All":
            sleep_moments = sleep_moments.groupby("Date", as_index=False)["SleepHours"].mean() # Average over all users
            title = "Sleep Duration Over Time For All Users"
            y_label = "Average Hours Slept"
        else:
            sleep_moments = Util.filter_by_user(sleep_moments, self.user)
            title = f"Sleep Duration Over Time For User {self.user}"
            y_label = "Hours Slept"

        fig = px.line(sleep_moments, x="Date", y="SleepHours", title=title, labels=dict(SleepHours=y_label))
        Util.overlay_no_data_on_graph_if_empty(sleep_moments, "SleepHours", fig)
        return fig

    def get_sedentary_hrs_to_sleep_hrs_regression(self) -> go.Figure:
        """Returns a Plotly figure of a regression between hours spent sedentary and hours slept."""
        sedentary_and_sleep_data = self.fitbit_db.get_sedentary_sleep_activity()

        sedentary_and_sleep_data = Util.filter_by_date_range(sedentary_and_sleep_data, self.start_date, self.end_date)
        title = "Relation Between Daily Sedentary Time And Sleep Duration For All Users"
        if self.user != "All":
            title = f"Relation Between Daily Sedentary Time and Sleep Duration For User {self.user}"
            sedentary_and_sleep_data = Util.filter_by_user(sedentary_and_sleep_data, self.user)

        fig = px.scatter(sedentary_and_sleep_data, x="SedentaryHours", y="HoursSlept", trendline="ols", title=title,
                         labels=dict(SedentaryHours="Sedentary Hours", HoursSlept="Hours Slept"), opacity=0.5)
        Util.overlay_no_data_on_graph_if_empty(sedentary_and_sleep_data, "HoursSlept", fig)
        return fig

    def get_active_hrs_to_sleep_hrs_regression(self, week_period: str = "") -> go.Figure:
        """Returns a Plotly figure of a regression between hours spent active and hours slept"""
        active_and_sleep_data = self.fitbit_db.get_active_and_sleep_hrs(week_period)

        active_and_sleep_data = Util.filter_by_date_range(active_and_sleep_data, self.start_date, self.end_date)
        title = "Relation Between Daily Active Time And Sleep Duration For All Users"
        if self.user != "All":
            title = f"Relation Between Daily Active Time And Sleep Duration For User {self.user}"
            active_and_sleep_data = Util.filter_by_user(active_and_sleep_data, self.user)

        fig = px.scatter(active_and_sleep_data, x="TotalActiveHours", y="TotalSleepHours", trendline="ols", title=title,
                         labels=dict(TotalActiveHours="Active Hours", TotalSleepHours="Hours Slept"), opacity=0.5)
        Util.overlay_no_data_on_graph_if_empty(active_and_sleep_data, "TotalSleepHours", fig)
        return fig

    def get_sleep_duration_per_time_blocks(self) -> go.Figure:
        """Returns a Plotly figure of a bar plot that divides a day into 6 4-hour time blocks and computes the average
        sleep duration per time block."""
        sleep_data = self.fitbit_db.get_daily_sleep_distribution()

        sleep_data = Util.filter_by_date_range(sleep_data, self.start_date, self.end_date)
        title = "Average Sleep Duration Per 4-Hour Time Blocks For All Users"
        if self.user != "All":
            sleep_data = Util.filter_by_user(sleep_data, self.user)
            title = f"Average Sleep Duration Per 4-Hour Time Blocks For User {self.user}"
        sleep_data = sleep_data.groupby("HourGroup", as_index=False, observed=False)["HoursSlept"].mean() # Average over all dates

        fig = px.bar(sleep_data, x="HourGroup", y="HoursSlept", title=title,
                     labels=dict(HourGroup="Time", HoursSlept="Average Hours Slept"))
        Util.overlay_no_data_on_graph_if_empty(sleep_data, "HoursSlept", fig)
        return fig

    def get_calories_burned_over_time(self) -> go.Figure:
        """Returns a Plotly figure that visualizes the number of calories burned each day."""
        calorie_data = self.fitbit_db.get_calories()

        calorie_data = Util.filter_by_date_range(calorie_data, self.start_date, self.end_date)
        if self.user == "All":
            calorie_data = calorie_data.groupby("Date", as_index=False)["Calories"].mean() # Average over all users
            title = "Calories Burned Over Time For All Users"
            y_label = "Average Calories Burned"
        else:
            calorie_data = Util.filter_by_user(calorie_data, self.user)
            title = f"Calories Burned Over Time For User {self.user}"
            y_label = "Calories Burned"

        fig = px.line(calorie_data, x="Date", y="Calories", title=title, labels=dict(Calories=y_label))
        Util.overlay_no_data_on_graph_if_empty(calorie_data, "Calories", fig)
        return fig

    def get_calories_burned_per_time_blocks(self) -> go.Figure:
        """Returns a Plotly figure of a bar plot that divides a day into 6 4-hour time blocks and computes the average
        calories burned per time block."""
        calorie_data = self.fitbit_db.get_daily_calorie_distribution()

        calorie_data = Util.filter_by_date_range(calorie_data, self.start_date, self.end_date)
        title = "Average Calories Burned Per 4-Hour Time Blocks For All Users"
        if self.user != "All":
            calorie_data = Util.filter_by_user(calorie_data, self.user)
            title = f"Average Calories Burned Per 4-Hour Time Blocks For User {self.user}"
        calorie_data = calorie_data.groupby("HourGroup", as_index=False, observed=False)["AverageCalories"].mean()  # Average over all dates

        fig = px.bar(calorie_data, x="HourGroup", y="AverageCalories", title=title,
                     labels=dict(HourGroup="Time", AverageCalories="Average Calories Burned"))
        Util.overlay_no_data_on_graph_if_empty(calorie_data, "AverageCalories", fig)
        return fig

    def get_heart_rate_over_time_and_average(self) -> (go.Figure, go.Figure):
        """Returns a Plotly figure that visualizes the heart rate each day."""
        if self.user == "All":
            heart_rate_data = self.fitbit_db.get_heart_rate_averaged_over_all_users()
            over_time_plot_title = "Heart Rate Over Time For All Users"
            over_time_plot_y_label = "Average Heart Rate (bpm)"
            average_plot_title = "Average Heart Rate" + "<br>" + "For All Users" + "<br>" + "Over Date Range"
        else:
            heart_rate_data = self.fitbit_db.get_heart_rate(self.user)
            over_time_plot_title = f"Heart Rate Over Time For User {self.user}"
            over_time_plot_y_label = "Heart Rate (bpm)"
            average_plot_title = "Average Heart Rate" + "<br>" + f"For User {self.user}" + "<br>" + "Over Date Range"

        heart_rate_data = Util.filter_by_date_range(heart_rate_data, self.start_date, self.end_date)
        heart_rate_data = heart_rate_data.sort_values(by="Date")  # Fix overlapping lines in plotly

        over_time_plot = px.line(heart_rate_data, x="Date", y="HeartRate", title=over_time_plot_title,
                                 labels=dict(HeartRate=over_time_plot_y_label))

        # Average over all dates
        avg_heart_rate = heart_rate_data.loc[:, "HeartRate"].mean()

        if np.isnan(avg_heart_rate):
            average_plot = go.Figure()
        else:
            avg_heart_rate = "{0:.2f}".format(avg_heart_rate) + " bpm"
            average_plot = go.Figure(go.Scatter(
                x=[0],
                y=[0],
                text=[avg_heart_rate],
                mode='text',
                textfont=dict(size=36),
            ))
        average_plot.update_layout(
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            title=average_plot_title,
            title_y=0.95
        )

        Util.overlay_no_data_on_graph_if_empty(heart_rate_data, "HeartRate", over_time_plot)
        Util.overlay_no_data_on_graph_if_empty(heart_rate_data, "HeartRate", average_plot)

        return over_time_plot, average_plot

    def plot_weight_change_vs_steps(self):
        """Generates a plot of weight change vs daily steps for a given user"""
        weight_data = self.fitbit_db.collect_weight_data()
        step_data = self.fitbit_db.get_daily_steps()
        weight_data = Util.filter_by_date_range(weight_data, self.start_date, self.end_date)
        step_data = Util.filter_by_date_range(step_data, self.start_date, self.end_date)
        weight_data = weight_data.set_index(['Id', 'Date'])

        idInData = True
        if self.user in weight_data.index.get_level_values(0):
            weight_data = weight_data.loc[self.user, ['Weight']]
            # Reindex step_data to be by date for a particular user
            step_data = step_data.loc[step_data.loc[:, 'Id'] == self.user].set_index('Date').loc[:, ['TotalSteps']]
        elif self.user == "All":
            weight_data = weight_data.groupby(level=1)['Weight'].mean().reset_index().set_index("Date")
            step_data = step_data.groupby('Date')['TotalSteps'].mean().reset_index().set_index("Date")
        else:
            df = step_data.groupby('Date')['TotalSteps'].mean().reset_index().set_index("Date")
            df['Weight'] = None
            idInData = False

        if idInData:
            # Reindex weight_data to match step_data and forward-fill missing values
            df = weight_data.reindex(step_data.index).ffill()
            # Join TotalSteps from step_data to df
            df = df.merge(step_data, on='Date', how='left')

        # Create subplots (3 plots: Weight vs Steps, Weight vs Date, Steps vs Date)
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=["Weight Over Time", "Steps Over Time"]
        )

        # Line plot: Weight vs. Date
        fig.add_trace(
            go.Scatter(x=df.index, y=df["Weight"], mode="lines+markers",
                    line=dict(color="red"), name="Weight vs Date"),
            row=1, col=1
        )

        # Line plot: Steps vs. Date
        fig.add_trace(
            go.Scatter(x=df.index, y=df["TotalSteps"], mode="lines+markers",
                    line=dict(color="green"), name="Steps vs Date"),
            row=1, col=2
        )

        # Update layout
        if self.user == "All":
            title_text = "Average weight and step analysis for all users"
        else:
            title_text = f"Weight & Steps Analysis for User {self.user}"

        fig.update_layout(
            title_text=title_text,
            showlegend=False
        )

        if self.user == "All":
            fig.update_yaxes(title_text="Average weight for all users (kg)", row=1, col=1)
        else:
            fig.update_yaxes(title_text="Weight (kg)", row=1, col=1)

        fig.update_xaxes(title_text="Date", row=1, col=1)

        if self.user == "All":
            fig.update_yaxes(title_text="Average steps for all users ", row=1, col=2)
        else:
            fig.update_yaxes(title_text="Steps per Day", row=1, col=2)

        fig.update_xaxes(title_text="Date", row=1, col=2)

        Util.overlay_no_data_on_graph_subplot_if_empty(df,"Weight", fig, row=1, col=1)
        Util.overlay_no_data_on_graph_subplot_if_empty(df, "TotalSteps", fig, row=1, col=2)

        return fig
