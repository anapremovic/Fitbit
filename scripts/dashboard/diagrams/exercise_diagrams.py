import datetime as datetime
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.formula.api as smf
import sklearn.linear_model as sk

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
        return fig

    def plot_steps_to_calories_regression(self, user_id: int): # Part 1: generate_steps_to_calories_regression
        data = self.fitbit_db.get_daily_activity()
        user_entries = data[data['UserId'] == user_id]
        
        least_squares_model = smf.ols(formula='Calories ~ TotalSteps + C(UserId)', data=data).fit()
        steps_coef = least_squares_model.params['TotalSteps']
        base_intercept = least_squares_model.params['Intercept']
        user_coef = least_squares_model.params.get(f'C(UserId)[T.{user_id}]', 0)

        regression_line = [base_intercept + user_coef + steps_coef * x for x in user_entries['TotalSteps']]

        fig = px.scatter(
            x=user_entries['TotalSteps'], 
            y=user_entries['Calories'], 
            title=f'Scatter plot of Steps Taken vs. Calories Burned for ID: {user_id}',
            labels={'x': 'Total Steps', 'y': 'Calories Burned'}
        )
        fig.add_trace(go.Scatter(x=user_entries['TotalSteps'], y=regression_line, mode='lines', name='Regression Line'))
        return fig

    def plot_weather_correlation_for_chicago(self): # Part 3: display_weather_correlation_for_chicago
        """
        Displays weather data for the city of Chicago and creates relationships between weather variables and activity.
        """
        self.chicago_data["datetime"] = pd.to_datetime(self.chicago_data["datetime"])
        
        daily_activity_db = self.fitbit_db.get_daily_activity()
        daily_activity_db["Date"] = pd.to_datetime(daily_activity_db["Date"])

        # Aggregate TotalDistance and Calories per day
        activity_agg = daily_activity_db.groupby("Date").agg(
            TotalDistance=("TotalDistance", "sum"),
            Calories=("Calories", "sum")
        ).reset_index()

        # Merge Fitbit and weather data
        merged_data = activity_agg.merge(self.chicago_data, left_on="Date", right_on="datetime")

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

            # Update layout of graph
            fig.update_layout(
                title=f"{ylabel} vs. {xlabel}",
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

    def plot_daily_step_distribution_barplot(self): # Part 3: generate_daily_step_distribution_barplot
        """Divide a day into 6 4-hour blocks and compute the average amount of steps
        taken per time block across all users. Visualize results in a bar plot."""
        
        step_data = self.fitbit_db.get_daily_step_distribution()

        return px.bar(
            step_data,
            x="HourGroup",
            y="AverageSteps",
            color_discrete_sequence=["green"],
            title="Average Number of Steps Taken per 4-Hour Time Block Across All Users",
            labels={"HourGroup": "Time", "AverageSteps": "Steps Taken"}
        )

    def plot_steps_to_heart_rate_and_avg_heart_rate(self, min_steps: int, max_steps: int): # Part 4
        """
        Plots daily steps vs heart rate regression and computes average heart rate for given step range
        """

        daily_steps_and_average_heart_rate_by_user = self.fitbit_db.get_daily_steps_and_average_heart_rate()
        x, y, regression_line = self.fit_regression(
            daily_steps_and_average_heart_rate_by_user, "TotalSteps", "AverageHeartRate"
        )
        avg_heart_rate = self.compute_avg_heart_rate(
            daily_steps_and_average_heart_rate_by_user, min_steps, max_steps
        )

        # Scatter plot of Daily Steps vs Average Heart Rate
        scatter_trace = go.Scatter(
            x=x.flatten(),
            y=y,
            mode="markers",
            marker=dict(color="green"),
            name="Observations"
        )

        # Regression line
        regression_trace = go.Scatter(
            x=x.flatten(),
            y=regression_line,
            mode="lines",
            line=dict(color="green"),
            name="Regression Line"
        )

        # Figure for the scatter plot
        fig1 = go.Figure([scatter_trace, regression_trace])
        fig1.update_layout(
            title="Relation Between Daily Steps and Average Heart Rate",
            xaxis_title="Daily Steps",
            yaxis_title="Average Daily Heart Rate (bpm)",
            template="plotly_white"
        )

        # Display Average Heart Rate for given step range
        if not np.isnan(avg_heart_rate):
            fig2 = go.Figure()
            fig2.add_trace(
                go.Indicator(
                    mode="number",
                    value=avg_heart_rate,
                    title={
                        "text": f"Average Heart Rate <br> for {min_steps} to {max_steps} steps",
                        "font": {"size": 16}
                    },
                    number={"font": {"size": 36}, "suffix": " bpm"}
                )
            )

        return fig1, fig2
    
    @staticmethod
    def fit_regression(data: pd.DataFrame, x_col: str, y_col: str):
        """Helper function to fit a regression to plot."""
        x = data.loc[:, [x_col]].values
        y = data.loc[:, y_col].values
        model = sk.LinearRegression()
        model.fit(x, y)
        regression_line = model.predict(x)

        return x, y, regression_line


    @staticmethod
    def compute_avg_heart_rate(data: pd.DataFrame, min_steps: int, max_steps: int):
        """Helper function to compute the average heart rate for users for given step range."""
        filtered_data = data[
            (data["TotalSteps"] >= min_steps) &
            (data["TotalSteps"] <= max_steps)
        ]
        return filtered_data["AverageHeartRate"].mean()
