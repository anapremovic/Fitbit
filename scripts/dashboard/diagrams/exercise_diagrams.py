# ----------
# Ensures that all Python files can be imported from any location
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_root)
# ----------

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.formula.api as smf
from scripts.database import FitbitDatabase

class ExerciseDiagrams:
    def __init__(self, fitbit_db: FitbitDatabase, chicago_csv: str):
        self.fitbit_db = fitbit_db
        
        self.chicago_data = pd.read_csv(os.path.join(project_root, chicago_csv))
        self.chicago_data["datetime"] = pd.to_datetime(self.chicago_data["datetime"])

    def plot_distance_walked_density(self):
        """Purpose: Create a density plot of the total distance walked by individuals"""
        data = self.fitbit_db.get_daily_activity()
        users = pd.unique(data.loc[:,'Id'])
        distances = [data.loc[data.loc[:, 'Id'] == user, 'TotalDistance'].sum() for user in users]

        fig = px.histogram(
            x=distances,
            nbins=30, 
            marginal='box', 
            histnorm='probability density',
            title='Density Plot of Walking Distances',
            labels={'x': 'Distance Walked (km)', 'y': 'Density'}
        )
        return fig

    def plot_day_of_week_frequency(self):
        """Create bar plot that displays the frequency of workouts per day of week"""
        data = self.fitbit_db.get_daily_activity()
        data["ActivityDate"] = pd.to_datetime(data.loc[:, "ActivityDate"])
        day_of_week_counts = data.loc[:, "ActivityDate"].dt.dayofweek.value_counts().sort_index()

        fig = px.bar(
            x=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            y=day_of_week_counts,
            title='Total Number of Workouts Per Day of Week',
            labels={'x': 'Day of the Week', 'y': 'Frequency'}
        )
        return fig

    def plot_steps_to_calories_regression(self, user_id: int):
        data = self.fitbit_db.get_daily_activity()
        user_entries = data[data['Id'] == user_id]
        
        least_squares_model = smf.ols(formula='Calories ~ TotalSteps + C(Id)', data=data).fit()
        steps_coef = least_squares_model.params['TotalSteps']
        base_intercept = least_squares_model.params['Intercept']
        user_coef = least_squares_model.params.get(f'C(Id)[T.{user_id}]', 0)

        regression_line = [base_intercept + user_coef + steps_coef * x for x in user_entries['TotalSteps']]

        fig = px.scatter(
            x=user_entries['TotalSteps'], 
            y=user_entries['Calories'], 
            title=f'Scatter plot of Steps Taken vs. Calories Burned for ID: {user_id}',
            labels={'x': 'Total Steps', 'y': 'Calories Burned'}
        )
        fig.add_trace(go.Scatter(x=user_entries['TotalSteps'], y=regression_line, mode='lines', name='Regression Line'))
        return fig

    def plot_weather_correlation_for_chicago(self):
        """
        Displays weather data for the city of Chicago and creates relationships between weather variables and activity.
        """
        self.chicago_data["datetime"] = pd.to_datetime(self.chicago_data["datetime"])
        
        daily_activity_db = self.fitbit_db.get_daily_activity()
        daily_activity_db["ActivityDate"] = pd.to_datetime(daily_activity_db["ActivityDate"])

        # Aggregate TotalDistance and Calories per day
        activity_agg = daily_activity_db.groupby("ActivityDate").agg(
            TotalDistance=("TotalDistance", "sum"),
            Calories=("Calories", "sum")
        ).reset_index()

        # Merge Fitbit and weather data
        merged_data = activity_agg.merge(self.chicago_data, left_on="ActivityDate", right_on="datetime")

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

            # Update layout with correlation in title
            fig.update_layout(
                title=f"{ylabel} vs. {xlabel} (Corr: {correlation:.3f})",
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

