import datetime as datetime
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from scripts.utils.style import Colors, Fonts
from scripts.utils.util import Util
from scripts.database import FitbitDatabase

class HealthDiagrams:
    def __init__(self, fitbit_db: FitbitDatabase, user, start_date: datetime, end_date: datetime):
        self.fitbit_db = fitbit_db
        self.user = user
        self.start_date = start_date
        self.end_date = end_date

    def get_sleep_duration_over_time_graph(self) -> go.Figure:
        """
        Create a line plot that displays the amount of sleep over time.
        """

        sleep_data = self.fitbit_db.get_sleep_durations()

        sleep_data = Util.filter_by_date_range(sleep_data, self.start_date, self.end_date)
        if self.user == "All":
            sleep_data = sleep_data.groupby("Date", as_index=False)["SleepHours"].mean() # Average over all users
            y_label = "Average Hours Slept"
        else:
            sleep_data = Util.filter_by_user(sleep_data, self.user)
            y_label = "Hours Slept"

        fig = px.line(
            sleep_data,
            x="Date",
            y="SleepHours",
            title="Sleep Duration Over Time",
            labels={"SleepHours": y_label},
            markers=True
        )
        fig.update_traces(line=dict(color=Colors.PRIMARY_COLOR))
        fig.update_layout(
            title=dict(
                x=0.55,
                xanchor="center"
            )
        )

        Util.show_no_data_if_empty(sleep_data, "SleepHours", fig)
        return fig

    def get_sedentary_hrs_to_sleep_hrs_regression(self) -> go.Figure:
        """
        Create a regression between hours spent sedentary and hours slept.
        """

        sedentary_and_sleep_data = self.fitbit_db.get_sedentary_sleep_activity()

        sedentary_and_sleep_data = Util.filter_by_date_range(sedentary_and_sleep_data, self.start_date, self.end_date)
        if self.user != "All":
            sedentary_and_sleep_data = Util.filter_by_user(sedentary_and_sleep_data, self.user)

        fig = px.scatter(
            sedentary_and_sleep_data,
            x="SedentaryHours",
            y="HoursSlept",
            trendline="ols",
            title="Relation Between Daily Sedentary Time And Sleep Duration",
            labels={"SedentaryHours": "Sedentary Hours", "HoursSlept": "Hours Slept"},
            opacity=0.6
        )
        fig.update_traces(marker_color=Colors.PRIMARY_COLOR)
        fig.update_layout(
            title=dict(
                x=0.55,
                xanchor="center"
            )
        )

        Util.show_no_data_if_empty(sedentary_and_sleep_data, "HoursSlept", fig)
        return fig

    def get_active_hrs_to_sleep_hrs_regression(self, week_period: str = "") -> go.Figure:
        """
        Create a regression between hours spent active and hours slept.
        """

        active_and_sleep_data = self.fitbit_db.get_active_and_sleep_hrs(week_period)

        active_and_sleep_data = Util.filter_by_date_range(active_and_sleep_data, self.start_date, self.end_date)
        if self.user != "All":
            active_and_sleep_data = Util.filter_by_user(active_and_sleep_data, self.user)

        fig = px.scatter(
            active_and_sleep_data,
            x="TotalActiveHours",
            y="TotalSleepHours",
            trendline="ols",
            title="Relation Between Daily Active Time And Sleep Duration",
            labels={"TotalActiveHours": "Active Hours", "TotalSleepHours": "Hours Slept"},
            opacity=0.6
        )
        fig.update_traces(marker_color=Colors.PRIMARY_COLOR)
        fig.update_layout(
            title=dict(
                x=0.5,
                xanchor="center"
            )
        )

        Util.show_no_data_if_empty(active_and_sleep_data, "TotalSleepHours", fig)
        return fig

    def get_sleep_duration_per_time_blocks_graph(self) -> go.Figure:
        """
        Create a bar plot that divides a day into 6 4-hour time blocks and
        computes the average sleep duration per time block.
        """

        sleep_data = self.fitbit_db.get_daily_sleep_distribution()

        sleep_data = Util.filter_by_date_range(sleep_data, self.start_date, self.end_date)
        if self.user != "All":
            sleep_data = Util.filter_by_user(sleep_data, self.user)

        num_distinct_sleep_sessions = sleep_data["logId"].nunique()
        sleep_data = sleep_data.groupby("HourGroup", as_index=False, observed=False)["HoursSlept"].sum()
        sleep_data["HoursSlept"] = np.divide(sleep_data["HoursSlept"], num_distinct_sleep_sessions)

        fig = px.bar(
            sleep_data,
            x="HourGroup",
            y="HoursSlept",
            title="Average Sleep Duration<br>Per 4-Hour Time Blocks",
            labels={"HourGroup": "Time", "HoursSlept": "Average Hours Slept"}
        )
        fig.update_traces(marker_color=Colors.PRIMARY_COLOR)
        fig.update_layout(
            xaxis=dict(tickangle=-45),
            title=dict(
                x=0.55,
                xanchor="center"
            )
        )

        Util.show_no_data_if_empty(sleep_data, "HoursSlept", fig)
        return fig

    def get_calories_burned_over_time_graph(self) -> go.Figure:
        """
        Create a line plot that displays the number of calories burned each day.
        """

        daily_activity = self.fitbit_db.get_daily_activity()

        daily_activity = Util.filter_by_date_range(daily_activity, self.start_date, self.end_date)
        if self.user == "All":
            daily_activity = daily_activity.groupby("Date", as_index=False)["Calories"].mean() # Average over all users
            y_label = "Average Calories Burned"
        else:
            daily_activity = Util.filter_by_user(daily_activity, self.user)
            y_label = "Calories Burned"

        fig = px.line(
            daily_activity,
            x="Date",
            y="Calories",
            title="Calories Burned Over Time",
            labels={"Calories": y_label},
            markers=True
        )
        fig.update_traces(line=dict(color=Colors.PRIMARY_COLOR))
        fig.update_layout(
            title=dict(
                x=0.55,
                xanchor="center"
            )
        )

        Util.show_no_data_if_empty(daily_activity, "Calories", fig)
        return fig

    def get_calories_burned_per_time_blocks_graph(self) -> go.Figure:
        """
        Create a bar plot that divides a day into 6 4-hour time blocks and
        computes the average calories burned per time block.
        """
        calorie_data = self.fitbit_db.get_daily_calorie_distribution()

        calorie_data = Util.filter_by_date_range(calorie_data, self.start_date, self.end_date)
        if self.user != "All":
            calorie_data = Util.filter_by_user(calorie_data, self.user)
        calorie_data = calorie_data.groupby("HourGroup", as_index=False, observed=False)["AverageCalories"].mean()  # Average over all dates

        fig = px.bar(
            calorie_data,
            x="HourGroup",
            y="AverageCalories",
            title="Average Calories Burned<br>Per 4-Hour Time Blocks",
            labels={"HourGroup": "Time", "AverageCalories": "Average Calories Burned"}
        )
        fig.update_traces(marker_color=Colors.PRIMARY_COLOR)
        fig.update_layout(
            xaxis=dict(tickangle=-45),
            title=dict(
                x=0.55,
                xanchor="center"
            )
        )

        Util.show_no_data_if_empty(calorie_data, "AverageCalories", fig)
        return fig

    def get_heart_rate_over_time_and_average_graphs(self) -> tuple[go.Figure, go.Figure]:
        """
        Create a line plot that displays the average heart rate each day.
        Also add a numerical value for the average heart rate over all days.
        """

        if self.user == "All":
            heart_rate_data = self.fitbit_db.get_heart_rate_averaged_over_all_users()
            over_time_plot_y_label = "Average Heart Rate (bpm)"
        else:
            heart_rate_data = self.fitbit_db.get_heart_rate(self.user)
            over_time_plot_y_label = "Heart Rate (bpm)"

        heart_rate_data = Util.filter_by_date_range(heart_rate_data, self.start_date, self.end_date)
        heart_rate_data = heart_rate_data.sort_values(by="Date")  # Fix overlapping lines in plotly

        over_time_plot = px.line(
            heart_rate_data,
            x="Date",
            y="HeartRate",
            title="Heart Rate Over Time",
            labels={"HeartRate": over_time_plot_y_label},
            markers=True
        )
        over_time_plot.update_traces(line=dict(color=Colors.PRIMARY_COLOR))
        over_time_plot.update_layout(
            xaxis=dict(tickangle=-45),
            title=dict(
                x=0.5,
                xanchor="center"
            )
        )

        # Average over all dates
        avg_heart_rate = heart_rate_data.loc[:, "HeartRate"].mean()

        if np.isnan(avg_heart_rate):
            average_plot = go.Figure()
        else:
            average_plot = go.Figure(go.Indicator(
                mode="number",
                value=round(avg_heart_rate, 2),
                number={"font": {"size": Fonts.LARGE_FONT_SIZE, "color": Colors.PRIMARY_COLOR}, "suffix": "bpm"}
            ))
        average_plot.update_layout(
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            title="Average Heart Rate<br>Over Date Range",
            title_y=0.95,
            title_x=0.55,
            title_xanchor="center"
        )

        Util.show_no_data_if_empty(heart_rate_data, "HeartRate", over_time_plot)
        Util.show_no_data_if_empty(heart_rate_data, "HeartRate", average_plot)
        return over_time_plot, average_plot

    def get_weight_and_steps_over_time_graphs(self) -> go.Figure:
        """
        Create line plots that display weight and steps over time.
        """

        weight_data = self.fitbit_db.get_weight_data()
        daily_activity = self.fitbit_db.get_daily_activity()

        weight_data = Util.filter_by_date_range(weight_data, self.start_date, self.end_date)
        daily_activity = Util.filter_by_date_range(daily_activity, self.start_date, self.end_date)
        weight_data = weight_data.set_index(["UserId", "Date"])

        has_data_available = True
        if self.user in weight_data.index.get_level_values(0):
            weight_data = weight_data.loc[self.user, ["Weight"]]
            # Reindex daily_activity to be by date for a particular user
            daily_activity = daily_activity.loc[daily_activity.loc[:, "UserId"] == self.user].set_index("Date").loc[:, ["TotalSteps"]]
        elif self.user == "All":
            weight_data = weight_data.groupby(level=1)["Weight"].mean().reset_index().set_index("Date")
            daily_activity = daily_activity.groupby("Date")["TotalSteps"].mean().reset_index().set_index("Date")
        else:
            df = daily_activity.loc[daily_activity.loc[:, "UserId"] == self.user].set_index("Date").loc[:, ["TotalSteps"]]
            df["Weight"] = None
            has_data_available = False

        if has_data_available:
            # Reindex weight_data to match step_data and forward-fill missing values
            df = weight_data.reindex(daily_activity.index).ffill()
            # Join TotalSteps from step_data to df
            df = df.merge(daily_activity, on="Date", how="left")

        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=["Weight Over Time", "Steps Over Time"]
        )

        # Line plot: Weight over time
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df["Weight"],
                mode="lines+markers",
                line=dict(color=Colors.PRIMARY_COLOR),
                name="Weight"
            ),
            row=1, col=1
        )

        # Line plot: Steps over time
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["TotalSteps"],
                mode="lines+markers",
                line=dict(color=Colors.PRIMARY_COLOR),
                name="Steps"
            ),
            row=1, col=2
        )

        fig.update_layout(
            title_text="Weight And Steps Over Time",
            showlegend=False,
            title=dict(
                x=0.5,
                xanchor="center"
            )
        )

        if self.user == "All":
            fig.update_yaxes(title_text="Average Weight (kg)", row=1, col=1)
            fig.update_yaxes(title_text="Average Daily Steps", row=1, col=2)
        else:
            fig.update_yaxes(title_text="Weight (kg)", row=1, col=1)
            fig.update_yaxes(title_text="Daily Steps", row=1, col=2)

        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_xaxes(title_text="Date", row=1, col=2)

        Util.show_no_data_if_empty_subplot(df, "Weight", fig, row=1, col=1)
        Util.show_no_data_if_empty_subplot(df, "TotalSteps", fig, row=1, col=2)

        return fig
