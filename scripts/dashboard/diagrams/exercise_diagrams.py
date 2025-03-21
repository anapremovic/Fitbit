import datetime as datetime
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.formula.api as smf

from scripts.dashboard.utils.util import Util
from scripts.database import FitbitDatabase

class ExerciseDiagrams:
    def __init__(self, fitbit_db: FitbitDatabase, chicago_csv: str):
        self.fitbit_db = fitbit_db
        
        self.chicago_data = pd.read_csv(chicago_csv)
        self.chicago_data["datetime"] = pd.to_datetime(self.chicago_data["datetime"])

    def plot_distance_walked_density(self, start_date: datetime, end_date: datetime): # Part 1: generate_distance_walked_density_plot
        """
        Purpose: Create a density plot of the total distance walked by individuals
        """

        data = self.fitbit_db.get_daily_activity()

        data = Util.filter_by_date_range(data, start_date, end_date)

        users = pd.unique(data.loc[:,'UserId'])
        distances = [data.loc[data.loc[:, 'UserId'] == user, 'TotalDistance'].sum() for user in users]

        fig = px.histogram(
            x=distances,
            nbins=30, 
            marginal='box', 
            histnorm='density',
            title="Distribution Of Distances Walked For All Users",
            labels={'x': 'Distance Walked (km)', 'y': 'Density'}
        )
        return fig

    def plot_day_of_week_frequency(self, user_id, start_date: datetime, end_date: datetime): # Part 1: generate_day_of_week_frequency_plot
        """
        Create bar plot that displays the frequency of workouts per day of week
        """

        data = self.fitbit_db.get_daily_activity()

        data = Util.filter_by_date_range(data, start_date, end_date)
        title = "Number Of Workouts Per Day Of Week Over All Users"
        if user_id != "All":
            data = Util.filter_by_user(data, user_id)
            title = f"Number Of Workouts Per Day Of Week For User {user_id}"

        day_of_week_counts = data.loc[:, "Date"].dt.dayofweek.value_counts().sort_index()
        # ensure y has 7 elements even if date range is under 7 days
        day_of_week_counts = day_of_week_counts.reindex(range(7), fill_value=0)

        fig = px.bar(
            x=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            y=day_of_week_counts,
            title=title,
            labels={'x': 'Day of the Week', 'y': 'Frequency'}
        )
        Util.overlay_no_data_on_graph_if_empty(data, fig)
        return fig

    def plot_steps_to_calories_regression(self, user_id, start_date: datetime, end_date: datetime): # Part 1: generate_steps_to_calories_regression
        data = self.fitbit_db.get_daily_activity()

        data = Util.filter_by_date_range(data, start_date, end_date)
        title = f"Relation Between Daily Steps And Calories Burned For All Users"
        if user_id != "All":
            data = Util.filter_by_user(data, user_id)
            title = f"Relation Between Daily Steps And Calories Burned For User {user_id}"
        
        least_squares_model = smf.ols(formula='Calories ~ TotalSteps + C(UserId)', data=data).fit()
        steps_coef = least_squares_model.params['TotalSteps']
        base_intercept = least_squares_model.params['Intercept']
        user_coef = least_squares_model.params.get(f'C(UserId)[T.{user_id}]', 0)

        regression_line = [base_intercept + user_coef + steps_coef * x for x in data['TotalSteps']]

        fig = px.scatter(
            x=data['TotalSteps'],
            y=data['Calories'],
            title=title,
            labels={'x': 'Total Steps', 'y': 'Calories Burned'}
        )
        fig.add_trace(go.Scatter(x=data['TotalSteps'], y=regression_line, mode='lines', name='Regression Line'))
        Util.overlay_no_data_on_graph_if_empty(data, fig)
        return fig

    def plot_weather_correlation_for_chicago(self, user_id, start_date: datetime, end_date: datetime): # Part 3: display_weather_correlation_for_chicago
        """
        Displays weather data for the city of Chicago and creates relationships between weather variables and activity.
        """
        self.chicago_data.rename(columns={"datetime": "Date"}, inplace=True)
        self.chicago_data["Date"] = pd.to_datetime(self.chicago_data["Date"])
        
        daily_activity_db = self.fitbit_db.get_daily_activity()

        self.chicago_data = Util.filter_by_date_range(self.chicago_data, start_date, end_date)
        daily_activity_db = Util.filter_by_date_range(daily_activity_db, start_date, end_date)
        if user_id != "All":
            daily_activity_db = Util.filter_by_user(daily_activity_db, user_id)

        # Aggregate TotalDistance and Calories per day
        activity_agg = daily_activity_db.groupby("Date").agg(
            TotalDistance=("TotalDistance", "sum"),
            Calories=("Calories", "sum")
        ).reset_index()

        # Merge Fitbit and weather data
        merged_data = activity_agg.merge(self.chicago_data, left_on="Date", right_on="Date")

        # Function to create scatter plot with best-fit line and correlation
        def scatter_with_fit(x, y, xlabel, ylabel, color):
            """
            Purpose: Helper function for plotting best-fit line
            """
            
            # Compute correlation
            correlation = x.corr(y)  # Pearson correlation

            # Compute regression line
            slope, intercept = np.polyfit(x, y, 1)
            y_pred = slope * np.array(x) + intercept  # Predicted values

            # Create figure
            fig = go.Figure()

            # Scatter plot
            fig.add_trace(go.Scatter(
                x=x, y=y, mode="markers", name="Data", marker=dict(color=color)
            ))

            # Best-fit line
            fig.add_trace(go.Scatter(
                x=x, y=y_pred, mode="lines", name="Best Fit Line", line=dict(color=color, dash="dash")
            ))

            if user_id == "All":
                title = f"Relation Between {xlabel} <br> And {ylabel} For All Users"
            else:
                title = f"Relation Between {xlabel} <br> And {ylabel} For User {user_id}"

            # Update layout of graph
            fig.update_layout(
                title=title,
                xaxis_title=xlabel,
                yaxis_title=ylabel
            )

            return fig, correlation

        figs = {}
        correlations = {}

        figs["distance_vs_temp"], correlations["distance_vs_temp"] = scatter_with_fit(
            merged_data["temp"], merged_data["TotalDistance"],
            xlabel="Temperature (°C)", ylabel="Total Distance (km)", color="red"
        )

        figs["calories_vs_temp"], correlations["calories_vs_temp"] = scatter_with_fit(
            merged_data["temp"], merged_data["Calories"],
            xlabel="Temperature (°C)", ylabel="Calories Burned", color="orange"
        )

        figs["distance_vs_precip"], correlations["distance_vs_precip"] = scatter_with_fit(
            merged_data["precip"], merged_data["TotalDistance"],
            xlabel="Precipitation (mm)", ylabel="Total Distance (km)", color="blue"
        )

        figs["calories_vs_precip"], correlations["calories_vs_precip"] = scatter_with_fit(
            merged_data["precip"], merged_data["Calories"],
            xlabel="Precipitation (mm)", ylabel="Calories Burned", color="green"
        )

        return figs, correlations

    def plot_daily_step_distribution_barplot(self, user_id, start_date: datetime, end_date: datetime): # Part 3: generate_daily_step_distribution_barplot
        """Divide a day into 6 4-hour blocks and compute the average amount of steps
        taken per time block across all users. Visualize results in a bar plot."""
        
        step_data = self.fitbit_db.get_daily_step_distribution()

        step_data = Util.filter_by_date_range(step_data, start_date, end_date)
        title = "Steps Taken Per 4-Hour Time Blocks For All Users"
        if user_id != "All":
            step_data = Util.filter_by_user(step_data, user_id)
            title = f"Steps Taken Per 4-Hour Time Blocks For User {user_id}"
        step_data = step_data.groupby("HourGroup", as_index=False, observed=False)["AverageSteps"].mean()  # Average over all dates

        fig = px.bar(
            step_data,
            x="HourGroup",
            y="AverageSteps",
            color_discrete_sequence=["green"],
            title=title,
            labels={"HourGroup": "Time", "AverageSteps": "Average Steps Taken"}
        )
        Util.overlay_no_data_on_graph_if_empty(step_data, fig)
        return fig

    def plot_steps_to_heart_rate_and_avg_heart_rate(self, user_id, start_date: datetime, end_date: datetime): # Part 4
        """
        Plots daily steps vs heart rate regression and computes average heart rate for given step range
        """

        daily_steps_and_average_heart_rate = self.fitbit_db.get_daily_steps_and_average_heart_rate()

        daily_steps_and_average_heart_rate = (
            Util.filter_by_date_range(daily_steps_and_average_heart_rate, start_date, end_date))
        regression_title = "Relation Between Daily Steps and Average Heart Rate For All Users"
        average_plot_title = f"Average Heart Rate <br> For All Users"
        if user_id != "All":
            daily_steps_and_average_heart_rate = (
                Util.filter_by_user(daily_steps_and_average_heart_rate, user_id))
            regression_title = f"Relation Between Daily Steps and Average Heart Rate For User {user_id}"
            average_plot_title = f"Average Heart Rate <br> For User {user_id}"

        avg_heart_rate = daily_steps_and_average_heart_rate["AverageHeartRate"].mean()

        fig1 = px.scatter(daily_steps_and_average_heart_rate, x="TotalSteps", y="AverageHeartRate", trendline="ols",
                          title=regression_title)

        # Figure for the scatter plot
        fig1.update_layout(
            title=regression_title,
            xaxis_title="Daily Steps",
            yaxis_title="Average Daily Heart Rate (bpm)",
            template="plotly_white"
        )

        # Display Average Heart Rate
        if np.isnan(avg_heart_rate):
            fig2 = go.Figure()
        else:
            avg_heart_rate = "{0:.2f}".format(avg_heart_rate) + " bpm"
            fig2 = go.Figure(go.Scatter(
                x=[0],
                y=[0],
                text=[avg_heart_rate],
                mode='text',
                textfont=dict(size=36),
            ))
        fig2.update_layout(
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            title={
                "text": average_plot_title,
                "font": {"size": 16}
            },
            title_y=0.95
        )

        Util.overlay_no_data_on_graph_if_empty(daily_steps_and_average_heart_rate, fig1)
        Util.overlay_no_data_on_graph_if_empty(daily_steps_and_average_heart_rate, fig2)

        return fig1, fig2
