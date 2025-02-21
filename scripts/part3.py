import database as db

import numpy as np
import scipy.stats as sp
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

def regression_sedentary_vs_sleep():
    """Analyses the relationship between the amount of sedentary activity and the
    sleep duration for all individuals by performing a linear regression on all
    data with the sleep duration as response variable and the the sedentary activity 
    as explanatory variables. """

    sedentary_sleep_data = db.get_sedentary_sleep_activity()
    least_squares_model = smf.ols(formula='MinutesSlept ~ SedentaryMinutes', data=sedentary_sleep_data).fit()
    intercept = least_squares_model.params['Intercept']
    slope = least_squares_model.params['SedentaryMinutes']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6), layout='tight')
    ax1.axline((0, intercept), slope=slope, label='Regression line')
    ax1.scatter(sedentary_sleep_data.loc[:, 'SedentaryMinutes'], sedentary_sleep_data.loc[:, 'MinutesSlept'], label='Observations')
    ax1.set_title('Relation Daily Sedentary Time and Time Slept \n Across All Users')
    ax1.set_xlabel('Sedentary Minutes')
    ax1.set_ylabel('Minutes Slept')
    ax1.legend()

    # Visually verifty errors are normally distributed
    residuals = least_squares_model.resid
    root_mse = np.sqrt(np.mean(residuals ** 2))
    range = np.arange(-600, 600, 5)
    norm_pdf = sp.norm.pdf(range, loc=0, scale=root_mse)
    ax2.hist(residuals, bins=20, range=(-600, 600), density=True, label='Residuals')
    ax2.plot(range, norm_pdf, label=r'$\mathcal{N}(0, \sqrt{MSE})$')
    ax2.set_title('Distribution of Residuals')
    ax2.set_xlabel('Residual')
    ax2.set_ylabel('Density')
    ax2.legend()
    plt.show()

regression_sedentary_vs_sleep()

def generate_daily_step_distribution_barplot():
    """Divide a day into 6 4-hour blocks and compute the average amount of steps
    taken per time block across all users. Visualize results in a bar plot."""
    
    step_data = db.get_daily_step_distribution()
    plt.bar(step_data.loc[:, 'HourGroup'], step_data.loc[:, 'AverageSteps'])
    plt.title('Average Number of Steps Taken pe;r 4-Hour Time Block \n Across All Users')
    plt.xlabel('Time')
    plt.ylabel('Average Steps')
    plt.show()

generate_daily_step_distribution_barplot()

def generate_daily_calorie_distribution_barplot():
    """Divide a day into 6 4-hour blocks and compute the average amount of calories
    burnt per time block across all users. Visualize results in a bar plot."""
    pass

def generate_daily_sleep_distribution_barplot():
    """Divide a day into 6 4-hour blocks and compute the average amount of minutes
    slept per time block across all users. Visualize results in a bar plot."""
    pass
