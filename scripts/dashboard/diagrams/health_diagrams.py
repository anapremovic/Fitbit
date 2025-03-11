import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

class HealthDiagrams:
    def __init__(self):
        self.fitbit_db = st.session_state["fitbit_db"]

    def sleep_quantity_over_time(self, user_id):
        """Returns a Matplotlib figure for the number of hours slept each day."""
        sleep_moments = self.fitbit_db.get_sleep_moments()

        if user_id == "All":
            sleep_moments.groupby("Date", as_index=False)["SleepHours"].mean() # Change to average sleep minutes
            title = "Sleep Quantity Over Time For All Users"
            y_label = "Average Hours Slept"
        else:
            sleep_moments = sleep_moments[sleep_moments.loc[:, "UserId"] == user_id] # Filter by user
            title = f"Sleep Quantity Over Time For User {user_id}"
            y_label = "Hours Slept"


        if sleep_moments.empty:
            return None

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
