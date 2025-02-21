import matplotlib.pyplot as plt
import datetime as datetime
import database as db
import sklearn.linear_model as sk

def generate_active_min_to_sleep_min_regression(date: datetime):
    """Generates a regression that shows how sleep minutes relate to active minutes for all users on a given day"""
    active_min = db.get_active_min_data()
    sleep_min = db.get_sleep_data()

    active_min = active_min[active_min.loc[:, 'Date'].dt.date == date.date()]
    sleep_min = sleep_min[sleep_min.loc[:, 'Date'].dt.date == date.date()]
    active_and_sleep_min_grouped_by_user = active_min.merge(sleep_min, on=['UserId', 'Date']).groupby('UserId').agg(
        TotalActiveMin=('TotalActiveMin', 'sum'),
        MinSlept=('MinSlept', 'sum')
    ).reset_index()
    if active_and_sleep_min_grouped_by_user.empty:
        print(f"No sleep and/or activity data on {date.date()}.")
        return

    x = active_and_sleep_min_grouped_by_user.loc[:, ['MinSlept']].values
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
