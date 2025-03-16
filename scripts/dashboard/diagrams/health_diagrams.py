import datetime as datetime
import seaborn as sns
import matplotlib.pyplot as plt

from scripts.database import FitbitDatabase

class HealthDiagrams:
    def __init__(self, fitbit_db: FitbitDatabase):
        self.fitbit_db = fitbit_db

    def get_sleep_duration_over_time(self, user_id, first_date: datetime, last_date: datetime) -> plt.Figure:
        """Returns a Matplotlib figure that visualizes the number of hours slept each day."""
        sleep_moments = self.fitbit_db.get_sleep_moments()

        # Filter Dates
        sleep_moments = sleep_moments[(sleep_moments["Date"] >= first_date) & (sleep_moments["Date"] <= last_date)]

        # Filter UserIds
        if user_id == "All":
            sleep_moments.groupby("Date", as_index=False)["SleepHours"].mean() # Change to average sleep minutes
            title = "Sleep Duration Over Time For All Users"
            y_label = "Average Hours Slept"
        else:
            sleep_moments = sleep_moments[sleep_moments.loc[:, "UserId"] == user_id] # Filter by user
            title = f"Sleep Duration Over Time For User {user_id}"
            y_label = "Hours Slept"

        if sleep_moments.empty:
            return plt.figure()

        fig = plt.figure(figsize=(10, 5))
        sns.lineplot(x=sleep_moments["Date"], y=sleep_moments["SleepHours"], marker="o", color="b")
        plt.title(title, fontsize=14)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel(y_label, fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True, prune='both', nbins=6))
        plt.grid(True)
        plt.tight_layout()
        return fig

    def plot_calories_burned(user_id: int, start_date: datetime = None, end_date: datetime = None):
        """
            Purpose: This function displays the calories burned for each day given a specific user's ID. 
            Can also set a date range to see a snapshot of the results. Otherwise, the entire duration of calories burned is shown 
        """
        data = self.fitbit_db.get_daily_activity()
        data_for_id = data.loc[data.loc[:, "Id"] == user_id ].copy()
        data_for_id["datetime"] = pd.to_datetime(data_for_id.loc[:,"ActivityDate"], errors="coerce") # Create datetime column
        # Set default time ranges
        if start_date is None:
            start_date = data_for_id["datetime"].min()
        if end_date is None:
            end_date = data_for_id["datetime"].max()
        # Ensure data is in between start and end dates
        data_for_id = data_for_id[
            (data_for_id.loc[:,"datetime"] >= start_date) & 
            (data_for_id.loc[:,"datetime"] <= end_date)
        ]

        # Setup pyplot
        fix, ax = plt.subplots(figsize=(12, 8))
        ax.plot(data_for_id["datetime"], data_for_id["Calories"], marker='o', linestyle="-")
        ax.set_xlabel("Date of Activity")
        ax.set_ylabel("Calories Burned")
        ax.set_title(f"Calories Burned per Day for ID: {user_id}")
        ax.xaxis.set_major_locator(mdates.DayLocator())

        ax.set_xticks(rotation = 30)
        return fig

    def plot_weight_change_vs_steps(weight_data, step_data, user_id: int):
        """Generates a plot of weight change vs daily steps for a given user"""
        weight_data = self.fitbit_db.collect_weight_data()
        step_data = self.fitbit_db.get_daily_steps()
        weight_data = weight_data.set_index(['Id', 'Date'])
        weight_data = weight_data.loc[user_id, ['Weight']]
        
        # Reindex step_data to be by date for a particular user
        step_data = step_data.loc[step_data.loc[:, 'Id'] == user_id].set_index('ActivityDate').loc[:, ['TotalSteps']]

        # Reindex weight_data to match step_data and forward-fill missing values
        df = weight_data.reindex(step_data.index).ffill()

        # Join TotalSteps from step_data to df
        df = df.join(step_data, how='left')

        
        # Plot weight change vs. daily steps
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(x=df["TotalSteps"], y=df["Weight"], edgecolor='black')

        ax.set_xlabel("Steps per Day")
        ax.set_ylabel("Weight (kg)")
        ax.set_title(f"Weight vs. Daily Steps for User {user_id}")
        ax.grid(True)
        return plt
