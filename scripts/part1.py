import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

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

    plt.xlabel('Total steps')
    plt.ylabel('Calories burned')
    plt.grid()
    plt.legend()
    plt.show()
