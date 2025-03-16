# ----------
# Ensures that all Python files can be imported from any location
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)
# ----------


import pandas as pd
# import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.formula.api as smf
from scripts.database import FitbitDatabase

class ExerciseDiagrams:
    def __init__(self, fitbit_db: FitbitDatabase, weather_csv: str):
        self.fitbit_db = fitbit_db
        self.chicago_data = pd.read_csv(weather_csv)
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

# def plot_weather_correlation_for_chicago(self, chicago_data):
#         """
#         Purpose: Displays weather data for the city of Chicago and creates a relationship between the variables
#         """
#         daily_activity_db = self.db.get_daily_activity()
#         # Connect to database and load Fitbit data
#         daily_activity_db["ActivityDate"] = pd.to_datetime(daily_activity_db["ActivityDate"])

#         # Aggregate TotalDistance and Calories per day
#         activity_agg = daily_activity_db.groupby("ActivityDate").agg(
#             TotalDistance=("TotalDistance", "sum"),
#             Calories=("Calories", "sum")
#         ).reset_index()

#         # Merge Fitbit and weather data
#         merged_data = activity_agg.merge(self.chicago_data, left_on="ActivityDate", right_on="datetime").loc[:, ["TotalDistance", "Calories", "temp", "precip"]]

#         # Compute Correlations
#         corr_temp_distance = merged_data["TotalDistance"].corr(merged_data["temp"])
#         corr_precip_distance = merged_data["TotalDistance"].corr(merged_data["precip"])
#         corr_temp_calories = merged_data["Calories"].corr(merged_data["temp"])
#         corr_precip_calories = merged_data["Calories"].corr(merged_data["precip"])

#         # Create subplots for visualizations
#         fig, axes = plt.subplots(2, 2, figsize=(12, 12))

#         # Scatter Plot: Temperature vs. Total Distance
#         sns.regplot(x=merged_data["temp"], y=merged_data["TotalDistance"], ax=axes[0, 0], color="red")
#         axes[0, 0].set_title(f"Temperature vs. Total Distance (Corr: {corr_temp_distance:.3f})")
#         axes[0, 0].set_xlabel("Temperature (°C)")
#         axes[0, 0].set_ylabel("Total Distance (km)")

#         # Scatter Plot: Precipitation vs. Total Distance
#         sns.regplot(x=merged_data["precip"], y=merged_data["TotalDistance"], ax=axes[0, 1], color="blue")
#         axes[0, 1].set_title(f"Precipitation vs. Total Distance (Corr: {corr_precip_distance:.3f})")
#         axes[0, 1].set_xlabel("Precipitation (mm)")
#         axes[0, 1].set_ylabel("Total Distance (km)")

#         # Scatter Plot: Temperature vs. Calories Burned
#         sns.regplot(x=merged_data["temp"], y=merged_data["Calories"], ax=axes[1, 0], color="orange")
#         axes[1, 0].set_title(f"Temperature vs. Calories Burned (Corr: {corr_temp_calories:.3f})")
#         axes[1, 0].set_xlabel("Temperature (°C)")
#         axes[1, 0].set_ylabel("Calories Burned")

#         # Scatter Plot: Precipitation vs. Calories Burned
#         sns.regplot(x=merged_data["precip"], y=merged_data["Calories"], ax=axes[1, 1], color="green")
#         axes[1, 1].set_title(f"Precipitation vs. Calories Burned (Corr: {corr_precip_calories:.3f})")
#         axes[1, 1].set_xlabel("Precipitation (mm)")
#         axes[1, 1].set_ylabel("Calories Burned")

#         fig.tight_layout()
        return fig

    def plot_weather_correlation_for_chicago(self):
        """
        Purpose: Displays weather data for the city of Chicago and creates a relationship between the variables
        """
        daily_activity_db = self.fitbit_db.get_daily_activity()
        # Connect to database and load Fitbit data
        daily_activity_db["ActivityDate"] = pd.to_datetime(daily_activity_db["ActivityDate"])

        # Aggregate TotalDistance and Calories per day
        activity_agg = daily_activity_db.groupby("ActivityDate").agg(
            TotalDistance=("TotalDistance", "sum"),
            Calories=("Calories", "sum")
        ).reset_index()

        # Merge Fitbit and weather data
        merged_data = activity_agg.merge(self.chicago_data, left_on="ActivityDate", right_on="datetime").loc[:, ["TotalDistance", "Calories", "temp", "precip"]]

        fig = px.scatter_matrix(
            merged_data, 
            dimensions=['TotalDistance', 'Calories', 'temp', 'precip'],
            title='Weather Correlation with Activity in Chicago',
            labels={'TotalDistance': 'Total Distance (km)', 'Calories': 'Calories Burned', 'temp': 'Temperature (°C)', 'precip': 'Precipitation (mm)'}
        )
        return fig
