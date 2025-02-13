import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

filename = 'daily_activity.csv'
df = pd.read_csv(filename)
df['Id'] = df['Id'].astype(str)  # Ensure Id is treated as a categorical variable


def visualize(id: str):
    # Find the best slope among all users 
    user_entries = df.loc[ df.loc[:, 'Id'] == id ]
    user_steps = user_entries.loc[:, 'TotalSteps']
    user_calories = user_entries.loc[:, 'Calories']

    plt.scatter(user_steps, user_calories, label='Observations')

    model = smf.ols(formula='Calories ~ TotalSteps + C(Id)', data=df).fit()
    print(model.params)

    base_intercept = model.params["Intercept"]
    steps_coef = model.params["TotalSteps"]
    # base_intercept is the OLS line's intercept for the reference user (first ID that appears in
    # the df).
    user_coef = model.params.get(f'C(Id)[T.{id}]', 0)

    y_intercept = (0, base_intercept + user_coef)
    plt.axline(y_intercept, slope=steps_coef, label='Regression line')

    plt.xlabel('Total steps')
    plt.ylabel('Calories burned')
    plt.grid()
    plt.legend()
    plt.show()


visualize(df.at[300, 'Id'])
