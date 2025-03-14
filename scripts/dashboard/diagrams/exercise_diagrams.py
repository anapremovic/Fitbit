import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statsmodels.formula.api as smf
import datetime as datetime
import seaborn as sns
from scripts.database import FitbitDatabase

class ExerciseDiagrams:
    def __init__(self, fitbit_db: FitbitDatabase):
        self.fitbit_db = fitbit_db

    def plot_distance_walked_density(self):
        """Purpose: Create a density plot of the total distance walked by individuals"""
        data = self.fitbit_db.get_daily_activity()
        users = pd.unique(data.loc[:,'Id'])
        distances = [data.loc[data.loc[:, 'Id'] == user, 'TotalDistance'].sum() for user in users]

        fig, ax = plt.subplots()

        #Clip the data at 0 as there are no users walking less than 0 kilometers
        #Reduce the bandwidth to prevent smoothing and create a more representative plot
        sns.kdeplot(distances, fill=True, color="blue", clip =(0, None), bw_adjust=1)

        ax.set_xlabel("Distance Walked (km)")
        ax.set_ylabel("Density")
        ax.set_title("Density Plot of Walking Distances")
        return fig

    def plot_day_of_week_frequency(self):
        """Create bar plot that displays the frequency of workouts per day of week"""
        data = self.fitbit_db.get_daily_activity()
        data["ActivityDate"] = pd.to_datetime(data.loc[:, "ActivityDate"])
        day_of_week_counts = data.loc[:, "ActivityDate"].dt.dayofweek.value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(day_of_week_counts.index, day_of_week_counts.values, color="green")
        ax.set_xticks(ticks=range(7), labels=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        ax.set_ylabel("Frequency")
        ax.set_title("Total Number of Workouts Per Day of Week")
        return fig

    def plot_steps_to_calories_regression(self, user_id: int):
        """Create a regression to visualize the relationship between
        the steps taken and the calories burned for a given user"""
        data = self.fitbit_db.get_daily_activity()
        user_entries = data.loc[data.loc[:, 'Id'] == user_id ]
        user_steps = user_entries.loc[:, 'TotalSteps']
        user_calories = user_entries.loc[:, 'Calories']

        fig, ax = plt.subplots()

        ax.scatter(user_steps, user_calories, color="green", label='Observations')

        least_squares_model = smf.ols(formula='Calories ~ TotalSteps + C(Id)', data=data).fit()
        base_intercept = least_squares_model.params["Intercept"]
        steps_coef = least_squares_model.params["TotalSteps"]
        user_coef = least_squares_model.params.get(f'C(Id)[T.{user_id}]', 0)

        y_intercept = (0, base_intercept + user_coef)
        ax.axline(y_intercept, slope=steps_coef, color="green", label='Regression line')

        ax.set_title(f'Scatter plot of Steps Taken vs. Calories Burned for ID: {user_id}')
        ax.set_xlabel('Total Steps')
        ax.set_ylabel('Calories Burned')
        ax.grid()
        ax.legend()

        return fig

    def plot_weather_correlation_for_chicago(self, chicago_data):
        """
        Purpose: Displays weather data for the city of Chicago and creates a relationship between the variables
        """
        daily_activity_db = self.db.get_daily_activity()
        # Connect to database and load Fitbit data
        daily_activity_db["ActivityDate"] = pd.to_datetime(daily_activity_db["ActivityDate"])

        # Aggregate TotalDistance and Calories per day
        activity_agg = daily_activity_db.groupby("ActivityDate").agg(
            TotalDistance=("TotalDistance", "sum"),
            Calories=("Calories", "sum")
        ).reset_index()

        # Merge Fitbit and weather data
        merged_data = activity_agg.merge(self.chicago_data, left_on="ActivityDate", right_on="datetime").loc[:, ["TotalDistance", "Calories", "temp", "precip"]]

        # Compute Correlations
        corr_temp_distance = merged_data["TotalDistance"].corr(merged_data["temp"])
        corr_precip_distance = merged_data["TotalDistance"].corr(merged_data["precip"])
        corr_temp_calories = merged_data["Calories"].corr(merged_data["temp"])
        corr_precip_calories = merged_data["Calories"].corr(merged_data["precip"])

        # Create subplots for visualizations
        fig, axes = plt.subplots(2, 2, figsize=(12, 12))

        # Scatter Plot: Temperature vs. Total Distance
        sns.regplot(x=merged_data["temp"], y=merged_data["TotalDistance"], ax=axes[0, 0], color="red")
        axes[0, 0].set_title(f"Temperature vs. Total Distance (Corr: {corr_temp_distance:.3f})")
        axes[0, 0].set_xlabel("Temperature (°C)")
        axes[0, 0].set_ylabel("Total Distance (km)")

        # Scatter Plot: Precipitation vs. Total Distance
        sns.regplot(x=merged_data["precip"], y=merged_data["TotalDistance"], ax=axes[0, 1], color="blue")
        axes[0, 1].set_title(f"Precipitation vs. Total Distance (Corr: {corr_precip_distance:.3f})")
        axes[0, 1].set_xlabel("Precipitation (mm)")
        axes[0, 1].set_ylabel("Total Distance (km)")

        # Scatter Plot: Temperature vs. Calories Burned
        sns.regplot(x=merged_data["temp"], y=merged_data["Calories"], ax=axes[1, 0], color="orange")
        axes[1, 0].set_title(f"Temperature vs. Calories Burned (Corr: {corr_temp_calories:.3f})")
        axes[1, 0].set_xlabel("Temperature (°C)")
        axes[1, 0].set_ylabel("Calories Burned")

        # Scatter Plot: Precipitation vs. Calories Burned
        sns.regplot(x=merged_data["precip"], y=merged_data["Calories"], ax=axes[1, 1], color="green")
        axes[1, 1].set_title(f"Precipitation vs. Calories Burned (Corr: {corr_precip_calories:.3f})")
        axes[1, 1].set_xlabel("Precipitation (mm)")
        axes[1, 1].set_ylabel("Calories Burned")

        fig.tight_layout()
        return fig