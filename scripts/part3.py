import matplotlib.pyplot as plt
import datetime as datetime
import database as db
import sklearn.linear_model as sk

def generate_active_min_to_sleep_min_regression(date: datetime):
    """Generates a regression that shows how sleep minutes relate to active minutes for all users on a given day"""
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
