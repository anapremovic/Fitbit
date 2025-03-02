import database as db
import matplotlib.pyplot as plt
import sklearn.linear_model as sk
import pandas as pd

def execute_part_4():
    """Generate all visualizations for part 4 of the project."""
    compare_sleep_to_active_min_relationship_for_week_periods()
    plot_daily_steps_to_average_heart_rate()

def compare_sleep_to_active_min_relationship_for_week_periods():
    """Generate three regressions to compare how sleep minutes affect active minutes on all days, weekdays only, and weekends only."""
    all_days = db.get_active_and_sleep_min()
    weekdays = db.get_active_and_sleep_min("weekdays")
    weekends = db.get_active_and_sleep_min("weekends")

    fig, axs = plt.subplots(1, 3, figsize=(24, 5))
    _plot_sleep_min_to_active_min(all_days, axs[0], "All Days")
    _plot_sleep_min_to_active_min(weekdays, axs[1], "Weekdays")
    _plot_sleep_min_to_active_min(weekends, axs[2], "Weekends")

    plt.tight_layout()
    plt.show()

def _plot_sleep_min_to_active_min(data: pd.DataFrame, axs: plt.Axes, week_period: str):
    """Helper function to plot one of the regressions in compare_sleep_to_active_min_relationship_for_week_periods()."""
    x = data.loc[:, ["TotalSleepMin"]].values
    y = data.loc[:, "TotalActiveMin"].values
    model = sk.LinearRegression()
    model.fit(x, y)
    regression_line = model.predict(x)

    axs.scatter(x, y, color="green", label="Observations")
    axs.plot(x, regression_line, color="green", label="Regression Line")
    axs.set_xlabel("Sleep Minutes")
    axs.set_ylabel("Active Minutes")
    axs.set_title(f"Regression of Sleep Minutes to Active Minutes on {week_period}")
    axs.legend()
    axs.grid(True)

def plot_daily_steps_to_average_heart_rate():
    daily_steps_and_average_heart_rate_by_user = db.get_daily_steps_and_average_heart_rate()

    x = daily_steps_and_average_heart_rate_by_user.loc[:, ["TotalSteps"]].values
    y = daily_steps_and_average_heart_rate_by_user.loc[:, "AverageHeartRate"].values
    model = sk.LinearRegression()
    model.fit(x, y)
    regression_line = model.predict(x)

    plt.scatter(x, y, color="green", label="Observations")
    plt.plot(x, regression_line, color="green", label="Regression Line")
    plt.xlabel("Daily Steps")
    plt.ylabel("Average Heart Rate")
    plt.title("Regression of Daily Steps to Average Heart Rate")
    plt.legend()
    plt.grid()
    plt.show()