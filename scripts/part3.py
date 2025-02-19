import database as db

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

def regression_sedentary_vs_sleep():
    sedentary_data = db.get_all_sedentary_activity()
    sleep_data = db.get_all_sleep_activity()
    sedentary_data = sedentary_data.rename(columns={'ActivityDate': 'date'})
    combined_data = pd.merge(sedentary_data, sleep_data, on=['Id', 'date'])
    plt.scatter(combined_data.loc[:, 'SedentaryMinutes'], combined_data.loc[:, 'minutesSlept'], label='Observations')

    least_squares_model = smf.ols(formula='minutesSlept ~ SedentaryMinutes', data=combined_data).fit()
    intercept = least_squares_model.params['Intercept']
    slope = least_squares_model.params['SedentaryMinutes']
    plt.axline((0, intercept), slope=slope, label='Regression line')

    plt.title('Relation Daily Sedentary Time and Time Slept \n Across All Users')
    plt.xlabel('Sedentary Minutes')
    plt.ylabel('Minutes Slept')
    plt.legend()
    plt.show()

regression_sedentary_vs_sleep()
