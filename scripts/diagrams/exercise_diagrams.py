import datetime as datetime
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from scripts.utils.style import Colors, Fonts
from scripts.utils.util import Util
from scripts.database import FitbitDatabase

class ExerciseDiagrams:
    def __init__(self, fitbit_db: FitbitDatabase, chicago_csv: str, user, start_date: datetime, end_date: datetime):
        self.fitbit_db = fitbit_db
        self.chicago_data = pd.read_csv(chicago_csv)
        self.chicago_data["Date"] = pd.to_datetime(self.chicago_data["Date"])
        self.user = user
        self.start_date = start_date
        self.end_date = end_date

    def get_distance_walked_density_graph(self) -> go.Figure:
        """
        Create a density plot of the total distance walked by individuals
        """

        daily_activity = self.fitbit_db.get_daily_activity()

        daily_activity = Util.filter_by_date_range(daily_activity, self.start_date, self.end_date)

        users = pd.unique(daily_activity.loc[:, "UserId"])
        distances = [daily_activity.loc[daily_activity.loc[:, "UserId"] == user, "TotalDistance"].sum() for user in users]

        fig = px.histogram(
            x=distances,
            nbins=30, 
            marginal="box",
            histnorm="density",
            title="Distribution Of Distances Walked For All Users",
            labels={"x": "Distance Walked (km)", "y": "Density"},
            color=Colors.PRIMARY_COLOR,
        )
        fig.update_layout(
            title=dict(
                x=0.55,
                xanchor="center"
            )
        )

        return fig

    def get_day_of_week_frequency_graph(self):
        """
        Create bar plot that displays the frequency of workouts per day of week.
        """

        daily_activity = self.fitbit_db.get_daily_activity()

        daily_activity = Util.filter_by_date_range(daily_activity, self.start_date, self.end_date)
        if self.user != "All":
            daily_activity = Util.filter_by_user(daily_activity, self.user)

        day_of_week_counts = daily_activity.loc[:, "Date"].dt.dayofweek.value_counts().sort_index()
        # ensure y has 7 elements even if date range is under 7 days
        day_of_week_counts = day_of_week_counts.reindex(range(7), fill_value=0)

        fig = px.bar(
            x=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            y=day_of_week_counts,
            title="Number Of Workouts Per Day Of Week",
            labels={"x": "Day of the Week", "y": "Frequency"},
        )
        fig.update_traces(marker_color=Colors.PRIMARY_COLOR)
        fig.update_layout(
            xaxis=dict(tickangle=-45),
            title=dict(
                x=0.55,
                xanchor="center"
            )
        )

        Util.show_no_data_if_empty(daily_activity, "Date", fig)
        return fig

    def get_steps_to_calories_regression(self) -> go.Figure:
        """
        Create a regression between daily steps and calories burned.
        """

        data = self.fitbit_db.get_daily_activity()

        data = Util.filter_by_date_range(data, self.start_date, self.end_date)
        if self.user != "All":
            data = Util.filter_by_user(data, self.user)

        fig = px.scatter(
            data,
            x="TotalSteps",
            y="Calories",
            title="Relation Between Daily Steps And Calories Burned",
            labels={"TotalSteps": "Total Steps", "Calories": "Calories Burned"},
            trendline="ols",
            opacity=0.6,
        )
        fig.update_traces(marker_color=Colors.PRIMARY_COLOR)
        fig.update_layout(
            title=dict(
                x=0.55,
                xanchor="center"
            )
        )

        Util.show_no_data_if_empty(data, "Calories", fig)
        return fig

    def get_weather_regressions(self) -> dict[str, go.Figure]:
        """
        Create regressions between weather variables and activity using weather data from the city of Chicago.
        """

        daily_activity = self.fitbit_db.get_daily_activity()

        self.chicago_data = Util.filter_by_date_range(self.chicago_data, self.start_date, self.end_date)
        daily_activity = Util.filter_by_date_range(daily_activity, self.start_date, self.end_date)
        if self.user != "All":
            daily_activity = Util.filter_by_user(daily_activity, self.user)

        activity_agg = daily_activity.groupby("Date").agg(
            TotalDistance=("TotalDistance", "mean"),
            Calories=("Calories", "mean")
        ).reset_index()

        merged_data = activity_agg.merge(self.chicago_data, left_on="Date", right_on="Date")

        def scatter_with_fit(data, x, y, x_label, y_label):
            """
            Helper function for plotting best-fit line
            """

            fig = px.scatter(
                data,
                x=x,
                y=y,
                trendline="ols",
                title=f"Relation Between {x_label} <br> And {y_label}",
                opacity=0.6
            )
            fig.update_layout(
                xaxis_title=x_label,
                yaxis_title=y_label,
                title=dict(
                    x=0.55,
                    xanchor="center"
                )
            )
            fig.update_traces(marker_color=Colors.PRIMARY_COLOR)

            return fig

        figs = {"distance_vs_temp": scatter_with_fit(
            data=merged_data, x="temp", y="TotalDistance",
            x_label="Temperature (°C)", y_label="Average Distance (km)"
        ), "calories_vs_temp": scatter_with_fit(
            data=merged_data, x="temp", y="Calories",
            x_label="Temperature (°C)", y_label="Average Calories Burned"
        )}

        Util.show_no_data_if_empty(merged_data, "TotalDistance", figs["distance_vs_temp"])
        Util.show_no_data_if_empty(merged_data, "Calories", figs["calories_vs_temp"])

        return figs

    def get_workout_frequency_by_weather_condition_graph(self) -> go.Figure:
        """
        Create a bar plot that displays the frequency of workout per weather condition in the city of Chicago.
        """

        daily_activity = self.fitbit_db.get_daily_activity()

        self.chicago_data = Util.filter_by_date_range(self.chicago_data, self.start_date, self.end_date)

        daily_activity = Util.filter_by_date_range(daily_activity, self.start_date, self.end_date)
        if self.user != "All":
            daily_activity = Util.filter_by_user(daily_activity, self.user)

        merged_data = pd.merge(daily_activity, self.chicago_data, on="Date", how="inner")
        merged_data["conditions"] = merged_data["conditions"].str.split(", ") # Split conditions column into list
        merged_data = merged_data.explode("conditions")  # Each condition becomes its own row

        condition_counts = merged_data["conditions"].value_counts()

        fig = px.bar(
            x=condition_counts.index,
            y=condition_counts.values,
            title="Number Of Workouts Per Weather Condition",
            labels={"x": "Weather Condition", "y": "Frequency"}
        )
        fig.update_traces(marker_color=Colors.PRIMARY_COLOR)
        fig.update_layout(
            xaxis=dict(tickangle=-45),
            title=dict(
                x=0.55,
                xanchor="center"
            )
        )

        Util.show_no_data_if_empty(merged_data, "conditions", fig)
        return fig

    def get_daily_steps_per_time_blocks_graph(self) -> go.Figure:
        """
        Create a bar plot that divides a day into 6 4-hour blocks
        and computes the average amount of steps taken per time block.
        """
        
        step_data = self.fitbit_db.get_daily_step_distribution()

        step_data = Util.filter_by_date_range(step_data, self.start_date, self.end_date)
        if self.user != "All":
            step_data = Util.filter_by_user(step_data, self.user)
        step_data = step_data.groupby("HourGroup", as_index=False, observed=False)["AverageSteps"].mean()  # Average over all dates

        fig = px.bar(
            step_data,
            x="HourGroup",
            y="AverageSteps",
            color_discrete_sequence=["green"],
            title="Average Steps Taken Per 4-Hour Time Blocks",
            labels={"HourGroup": "Time", "AverageSteps": "Average Steps Taken"}
        )
        fig.update_traces(marker_color=Colors.PRIMARY_COLOR)
        fig.update_layout(
            xaxis=dict(tickangle=-45),
            title=dict(
                x=0.55,
                xanchor="center"
            )
        )

        Util.show_no_data_if_empty(step_data, "AverageSteps", fig)
        return fig

    def get_steps_to_heart_rate_and_avg_heart_rate_graphs(self) -> tuple[go.Figure, go.Figure]:
        """
        Create regression between daily steps and average heart rate.
        Also add a numerical value for the average heart rate.
        """

        daily_steps_and_average_heart_rate = self.fitbit_db.get_daily_steps_and_average_heart_rate()

        daily_steps_and_average_heart_rate = (
            Util.filter_by_date_range(daily_steps_and_average_heart_rate, self.start_date, self.end_date))

        average_plot_title = f"Average Heart Rate <br> For All Users"
        if self.user != "All":
            daily_steps_and_average_heart_rate = (
                Util.filter_by_user(daily_steps_and_average_heart_rate, self.user))
            average_plot_title = f"Average Heart Rate <br> For User {self.user}"

        avg_heart_rate = daily_steps_and_average_heart_rate["AverageHeartRate"].mean()

        graph = px.scatter(
            daily_steps_and_average_heart_rate, 
            x="TotalSteps", 
            y="AverageHeartRate", 
            trendline="ols",
            title="Relation Between Daily Steps and Average Heart Rate",
            opacity=0.6,
        )
        graph.update_layout(
            xaxis_title="Daily Steps",
            yaxis_title="Average Daily Heart Rate (bpm)",
            template="plotly_white",
            title=dict(
                x=0.55,
                xanchor="center"
            )
        )
        graph.update_traces(marker_color=Colors.PRIMARY_COLOR)

        if np.isnan(avg_heart_rate):
            numerical = go.Figure()
        else:
            numerical = go.Figure(go.Scatter(
                x=[0],
                y=[0],
                text=[avg_heart_rate],
                mode='text',
                textfont=dict(size=36),
            ))
            numerical = go.Figure(go.Indicator(
                mode="number",
                value=round(avg_heart_rate, 2),
                number={"font": {"size": Fonts.LARGE_FONT_SIZE, "color": Colors.PRIMARY_COLOR}, "suffix": "bpm"}
            ))
            numerical.update_layout(
                showlegend=False,
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                title={
                    "text": average_plot_title,
                    "font": {"size": 16}
                },
                title_y=0.95,
            )

        Util.show_no_data_if_empty(daily_steps_and_average_heart_rate, "AverageHeartRate", graph)
        Util.show_no_data_if_empty(daily_steps_and_average_heart_rate, "AverageHeartRate", numerical)

        return graph, numerical
