import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as datetime
import database as db
import sklearn.linear_model as sk


def execute_part_3():
    """Generate all visualizations for part 3 of the project."""
    verify_correctness(db.get_daily_steps(), db.get_hourly_steps())
    generate_sleep_data_over_time_line_plot(6962181067)
    generate_active_min_to_sleep_min_regression(datetime.datetime(2016, 4, 1))

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

def verify_correctness(daily_data: pd.DataFrame, hourly_data: pd.DataFrame):
    daily_data_2 = hourly_data.groupby(['Id', 'ActivityDate'], as_index=False).sum()

    # Find common (Id, Date) pairs in both DataFrames
    common_keys = daily_data.loc[:, ['Id', 'ActivityDate']].merge(daily_data_2.loc[:, ['Id', 'ActivityDate']], how='inner')

    # Filter both DataFrames to keep only rows with common (Id, Date) pairs
    df1_common = daily_data.merge(common_keys, on=['Id', 'ActivityDate'])
    df2_common = daily_data_2.merge(common_keys, on=['Id', 'ActivityDate'])

    # Sort by Id and Date
    df1_common_sorted = df1_common.sort_values(by=['Id', 'ActivityDate']).reset_index(drop=True)
    df2_common_sorted = df2_common.sort_values(by=['Id', 'ActivityDate']).reset_index(drop=True)

    print('Is the data correct? ' + str(df1_common_sorted.equals(df2_common_sorted)))

    #Identify for rows with differences
    differences = df1_common_sorted.compare(df2_common_sorted)
    
    #Use conflict indexes to create a new conflicting_data DataFrame
    conflicting_data = df1_common_sorted.loc[differences.index, ['Id', 'ActivityDate']]
    conflicting_data.loc[:, 'HourlySteps'] = df1_common_sorted.loc[differences.index, ['TotalSteps']]
    conflicting_data.loc[:, 'DailySteps'] = df2_common_sorted.loc[differences.index, ['TotalSteps']]

    # Print the specific users and dates where conflicts occur
    print('Conflicts found for the following users and dates:')
    print(conflicting_data)

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
