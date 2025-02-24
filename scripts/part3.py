import database as db

import numpy as np
import pandas as pd
import datetime as datetime
import seaborn as sns
import scipy.stats as sp
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import sklearn.linear_model as sk

def visualize_part_3():
    """Generate all visualizations for part 3 of the project."""

    generate_sleep_data_over_time_line_plot(6962181067)
    generate_active_min_to_sleep_min_regression(datetime.datetime(2016, 4, 1))
    generate_sedentary_min_to_sleep_min_regression()
    generate_daily_step_distribution_barplot()
    generate_daily_calorie_distribution_barplot()
    generate_daily_sleep_distribution_barplot()

def generate_sleep_data_over_time_line_plot(user_id: float):
    """Generates a line plot which visualizes sleep data over time for a given user."""

    sleep_moments_for_user = db.get_sleep_moments(user_id)
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

def generate_active_min_to_sleep_min_regression(date: datetime):
    """Generates a regression that shows how sleep minutes relate to active minutes for all users on a given day."""

    active_and_sleep_min_grouped_by_user = db.get_active_and_sleep_min_grouped_by_user(date)
    if active_and_sleep_min_grouped_by_user.empty:
        print(f"No activity and/or sleep data on {date.date()}.")
        return

    x = active_and_sleep_min_grouped_by_user.loc[:, ['TotalSleepMin']].values
    y = active_and_sleep_min_grouped_by_user.loc[:, 'TotalActiveMin'].values
    model = sk.LinearRegression()
    model.fit(x, y)
    regression_line = model.predict(x)

    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, color='green', label='Observations')
    plt.plot(x, regression_line, color='green', label=f'Regression Line')
    plt.xlabel("Sleep Minutes")
    plt.ylabel("Active Minutes")
    plt.title(f"Regression of Sleep Minutes to Active Minutes on {date.date()}")
    plt.legend()
    plt.grid()
    plt.show()

def generate_sedentary_min_to_sleep_min_regression():
    """Analyses the relationship between the amount of sedentary activity and the
    sleep duration for all individuals by performing a linear regression on all
    data with the sleep duration as response variable and the the sedentary activity 
    as explanatory variables. """

    sedentary_sleep_data = db.get_sedentary_sleep_activity()

    least_squares_model = smf.ols(formula='MinutesSlept ~ SedentaryMinutes', data=sedentary_sleep_data).fit()
    intercept = least_squares_model.params['Intercept']
    slope = least_squares_model.params['SedentaryMinutes']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6), layout='tight')
    ax1.scatter(sedentary_sleep_data.loc[:, 'SedentaryMinutes'], sedentary_sleep_data.loc[:, 'MinutesSlept'], 
                color='C0', label='Observations')
    ax1.axline((0, intercept), slope=slope, color='C0', label='Regression line')
    ax1.set_title('Relation Daily Sedentary Time and Time Slept \n Across All Users')
    ax1.set_xlabel('Sedentary Minutes')
    ax1.set_ylabel('Minutes Slept')
    ax1.legend()

    # Visually verifty errors are normally distributed
    residuals = least_squares_model.resid
    root_mse = np.sqrt(np.mean(residuals ** 2))
    range = np.arange(-600, 600, 5)
    norm_pdf = sp.norm.pdf(range, loc=0, scale=root_mse)
    ax2.hist(residuals, bins=20, range=(-600, 600), 
             color='C0', density=True, label='Residuals')
    ax2.plot(range, norm_pdf, color='C1', label=r'$\mathcal{N}(0, \sqrt{MSE})$')
    ax2.set_title('Distribution of Residuals')
    ax2.set_xlabel('Residual')
    ax2.set_ylabel('Density')
    ax2.legend()
    plt.show()

def generate_daily_step_distribution_barplot():
    """Divide a day into 6 4-hour blocks and compute the average amount of steps
    taken per time block across all users. Visualize results in a bar plot."""
    
    step_data = db.get_daily_step_distribution()

    plt.bar(step_data.loc[:, 'HourGroup'], step_data.loc[:, 'AverageSteps'],
            color='C2')
    plt.title('Average Number of Steps Taken per 4-Hour Time Block \n Across All Users')
    plt.xlabel('Time')
    plt.ylabel('Steps Taken')
    plt.show()

def generate_daily_calorie_distribution_barplot():
    """Divide a day into 6 4-hour blocks and compute the average amount of calories
    burnt per time block across all users. Visualize results in a bar plot."""

    calorie_data = db.get_daily_calorie_distribtion()

    plt.bar(calorie_data.loc[:, 'HourGroup'], calorie_data.loc[:, 'AverageCalories'],
            color='C3')
    plt.title('Average Number of Calories Burnt per 4-Hour Time Block \n Across All Users')
    plt.xlabel('Time')
    plt.ylabel('Calories Burnt')
    plt.show()

def generate_daily_sleep_distribution_barplot():
    """Divide a day into 6 4-hour blocks and compute the average amount of minutes
    slept per time block across all users. Visualize results in a bar plot."""

    sleep_data = db.get_daily_sleep_distribution()

    plt.bar(sleep_data.loc[:, 'HourGroup'], sleep_data.loc[:, 'AverageMinutesSlept'],
            color='C4')
    plt.title('Average Number of Minutes Slept per 4-Hour Time Block \n Across All Users')
    plt.xlabel('Time')
    plt.ylabel('Minutes Slept')
    plt.show()

generate_sedentary_min_to_sleep_min_regression()
generate_daily_step_distribution_barplot()
generate_daily_calorie_distribution_barplot()
generate_daily_sleep_distribution_barplot()
