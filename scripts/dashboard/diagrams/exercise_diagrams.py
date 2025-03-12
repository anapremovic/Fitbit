import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statsmodels.formula.api as smf
import datetime as datetime
import seaborn as sns

def plot_distance_walked_density(data):
    """Purpose: Create a density plot of the total distance walked by individuals"""
    users = pd.unique(data.loc[:,'Id'])
    distances = []
    for user in users:
        distances.append(
            data.loc[ data.loc[:,'Id'] == user, 'TotalDistance' ].sum()
        )

    #Clip the data at 0 as there are no users walking less than 0 kilometers
    #Reduce the bandwidth to prevent smoothing and create a more representative plot
    sns.kdeplot(distances, fill=True, color="blue", clip =(0, None), bw_adjust=1)

    plt.xlabel("Distance Walked (km)")
    plt.ylabel("Density")
    plt.title("Density Plot of Walking Distances")
    return plt

def plot_calories_burned(data, user_id: int, start_date: datetime = None, end_date: datetime = None):
    """
    Purpose: This function displays the calories burned for each day given a specific user's ID. 
    Can also set a date range to see a snapshot of the results. Otherwise, the entire duration of calories burned is shown 
    """
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
    plt.figure(figsize=(12, 8))
    plt.plot(data_for_id["datetime"], data_for_id["Calories"], marker='o', linestyle="-")
    plt.xlabel("Date of Activity")
    plt.ylabel("Calories Burned")
    plt.title(f"Calories Burned per Day for ID: {user_id}")
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())  # set ticks for each day

    plt.xticks(rotation = 30)
    return plt