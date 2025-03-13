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
