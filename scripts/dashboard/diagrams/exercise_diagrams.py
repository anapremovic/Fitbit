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

def plot_day_of_week_frequency(data):
    """Create bar plot that displays the frequency of workouts per day of week"""
    data["ActivityDate"] = pd.to_datetime(data.loc[:, "ActivityDate"])
    day_of_week_counts = data.loc[:, "ActivityDate"].dt.dayofweek.value_counts().sort_index()

    plt.figure(figsize=(8, 5))
    plt.bar(day_of_week_counts.index, day_of_week_counts.values, color="green")
    plt.xticks(ticks=range(7), labels=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    plt.ylabel("Frequency")
    plt.title("Total Number of Workouts Per Day of Week")
    return plt

def generate_steps_to_calories_regression(data, user_id: int):
    """Create a regression to visualize the relationship between
    the steps taken and the calories burned for a given user"""
    user_entries = data.loc[data.loc[:, 'Id'] == user_id ]
    user_steps = user_entries.loc[:, 'TotalSteps']
    user_calories = user_entries.loc[:, 'Calories']

    plt.scatter(user_steps, user_calories, color="green", label='Observations')

    least_squares_model = smf.ols(formula='Calories ~ TotalSteps + C(Id)', data=data).fit()
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
    return plt