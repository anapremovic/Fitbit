import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statsmodels.formula.api as smf
import datetime as datetime
import seaborn as sns

def calc_num_users(data: pd.DataFrame,):
  """Calculates the total number of unique users in the dataset"""
  users = pd.unique(data.loc[:,'Id'])
  return len(users)

def generate_density_plot(data: pd.DataFrame,):
    """Create a density plot of the total distance walked by individuals"""
    users = pd.unique(data.loc[:,'Id'])
    distances = []
    for user in users:
        distances.append(data.loc[data.loc[:,'Id'] == user, 'TotalDistance'].sum())

    #Clip the data at 0 as there are no users walking less than 0 kilometers
    #Reduce the bandwidth to prevent smoothing and create a more representative plot
    sns.kdeplot(distances, fill=True, color="blue", clip =(0, None), bw_adjust=1)

    plt.xlabel("Distance Walked (km)")
    plt.ylabel("Density")
    plt.title("Density Plot of Walking Distances")

    plt.show()

def generate_distance_histogram(data: pd.DataFrame,):
    """Create a histogram describing the frequency of the distance 
    walked by individuals"""
    users = pd.unique(data.loc[:,'Id'])
    distances = []
    for user in users:
        distances.append(data.loc[data.loc[:,'Id'] == user, 'TotalDistance'].sum())
    bins = np.arange(0, max(distances), 15)
    plt.hist(distances, bins=bins, edgecolor='black') 
    plt.xticks(bins)
    plt.xlim(min(bins), max(bins))
    plt.xlabel("Distance Walked (km)")
    plt.ylabel("Frequency")
    plt.title("Histogram Plot of Walking Distances")

    plt.show()

def show_calories_per_day(data: pd.DataFrame, id: int, start_date: datetime = None, end_date: datetime = None):
    """
    Purpose: This function displays the calories burned for each day given a specific user's ID. Can also set a date range to see a snapshot of the results. Otherwise, the entire duration of calories burned is shown 

    Author: L.D. Lee
    """
    get_data_for_id = data.loc[data.loc[:, "Id"] == id].copy()
    get_data_for_id["datetime"] = pd.to_datetime(get_data_for_id.loc[:, "ActivityDate"]) # Create datetime column

    # Set default time ranges
    if (start_date == None): start_date = get_data_for_id["datetime"].min()
    if (end_date == None): end_date = get_data_for_id["datetime"].max()

    # Ensure data is in between start and end dates
    get_data_for_id = get_data_for_id[(get_data_for_id.loc[:, "datetime"] >= start_date) & (get_data_for_id.loc[:, "datetime"] <= end_date)]

    # Setup pyplot
    plt.figure(figsize=(12, 8))
    plt.plot(get_data_for_id["datetime"], get_data_for_id["Calories"], marker='o', linestyle="-")
    plt.xlabel("Date of Activity")
    plt.ylabel("Calories Burned")
    plt.title(f"Calories Burned per Day for ID: {id}")
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())  # set ticks for each day
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format as YYYY-MM-DD

    plt.xticks(rotation = 30)
    plt.show()


def generate_day_of_week_frequency_plot(daily_activity: DataFrame):
    daily_activity["ActivityDate"] = pd.to_datetime(daily_activity.loc[:, "ActivityDate"])
    day_of_week_counts = daily_activity.loc[:, "ActivityDate"].dt.dayofweek.value_counts().sort_index()

    plt.figure(figsize=(8, 5))
    plt.bar(day_of_week_counts.index, day_of_week_counts.values, color="green")
    plt.xticks(ticks=range(7), labels=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    plt.ylabel("Frequency")
    plt.title("Total Number of Workouts Per Day of Week")
    plt.show()

def generate_regression_line_for_user(daily_activity: DataFrame, user_id: str):
    user_entries = daily_activity.loc[ daily_activity.loc[:, 'Id'] == user_id ]
    user_steps = user_entries.loc[:, 'TotalSteps']
    user_calories = user_entries.loc[:, 'Calories']

    plt.scatter(user_steps, user_calories, color="green", label='Observations')

    least_squares_model = smf.ols(formula='Calories ~ TotalSteps + C(Id)', data=daily_activity).fit()
    base_intercept = least_squares_model.params["Intercept"]
    steps_coef = least_squares_model.params["TotalSteps"]
    user_coef = least_squares_model.params.get(f'C(Id)[T.{user_id}]', 0)

    y_intercept = (0, base_intercept + user_coef)
    plt.axline(y_intercept, slope=steps_coef, color="green", label='Regression line')

    plt.title(f'Scatter plot of Steps Taken vs. Calories Burned for ID: {user_id}')
    plt.xlabel('Total steps')
    plt.ylabel('Calories burned')
    plt.grid()
    plt.legend()
    plt.show()
