import streamlit as st

from scripts.database import FitbitDatabase

fitbit_db: FitbitDatabase = st.session_state["fitbit_db"]



"""
    def generate_sleep_data_over_time_line_plot(self, user_id: float):
        Generates a line plot which visualizes sleep data over time for a given user.

        sleep_moments_for_user = self.db.get_sleep_moments(user_id)
        if sleep_moments_for_user.empty:
            print(f"No sleep data found for User {user_id}.")
            return

        plt.figure(figsize=(10, 5))
        sns.lineplot(x=sleep_moments_for_user["Date"], y=sleep_moments_for_user["SleepMin"], marker="o", color="b")
        plt.title(f"Sleep Over Time for User {user_id}", fontsize=14)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Minutes Slept", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True, prune='both', nbins=6))
        plt.grid(True)
        plt.tight_layout()
        plt.show()
"""