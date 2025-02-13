import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt

daily_activity = pd.read_csv("data/daily_activity.csv", index_col=0)

def generate_day_of_week_frequency_plot(daily_activity: DataFrame):
    daily_activity["ActivityDate"] = pd.to_datetime(daily_activity.loc[:, "ActivityDate"])
    day_of_week_counts = daily_activity.loc[:, "ActivityDate"].dt.dayofweek.value_counts().sort_index()

    plt.figure(figsize=(8, 5))
    plt.bar(day_of_week_counts.index, day_of_week_counts.values, color="green")
    plt.xticks(ticks=range(7), labels=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    plt.ylabel("Frequency")
    plt.title("Total Number of Workouts Per Day of Week")
    plt.show()

generate_day_of_week_frequency_plot(daily_activity)