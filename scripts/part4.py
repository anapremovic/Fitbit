import database as db
import matplotlib.pyplot as plt
import sklearn.linear_model as sk
import pandas as pd
import numpy as np

def execute_part_4():
    """Generate all visualizations for part 4 of the project."""
    compare_sleep_to_active_min_relationship_for_week_periods()
    plot_steps_to_heart_rate_and_avg_heart_rate(10000, 15000)

def compare_sleep_to_active_min_relationship_for_week_periods():
    """Generate three regressions to compare how sleep minutes affect active minutes on all days, weekdays only, and weekends only."""
    all_days = db.get_active_and_sleep_min()
    weekdays = db.get_active_and_sleep_min("weekdays")
    weekends = db.get_active_and_sleep_min("weekends")

    fig, axs = plt.subplots(1, 3, figsize=(24, 5))
    plot_sleep_min_to_active_min(all_days, axs[0], "All Days")
    plot_sleep_min_to_active_min(weekdays, axs[1], "Weekdays")
    plot_sleep_min_to_active_min(weekends, axs[2], "Weekends")

    plt.tight_layout()
    plt.show()

def plot_steps_to_heart_rate_and_avg_heart_rate(min_steps: int, max_steps: int):
    """Plots daily steps vs heart rate regression and computes average heart rate for given step range."""
    daily_steps_and_average_heart_rate_by_user = db.get_daily_steps_and_average_heart_rate()
    x, y, regression_line = fit_regression(daily_steps_and_average_heart_rate_by_user, "TotalSteps", "AverageHeartRate")
    avg_heart_rate = compute_avg_heart_rate(daily_steps_and_average_heart_rate_by_user, min_steps, max_steps)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].scatter(x, y, color="green", label="Observations")
    axes[0].plot(x, regression_line, color="green", label="Regression Line")
    axes[0].set_xlabel("Daily Steps")
    axes[0].set_ylabel("Average Daily Heart Rate (bpm)")
    axes[0].set_title("Daily Steps vs. Average Heart Rate")
    axes[0].legend()
    axes[0].grid()

    axes[1].axis("off")
    if not np.isnan(avg_heart_rate):
        axes[1].set_title("Average Daily Heart Rate", fontsize=16, fontweight="bold", pad=20)
        axes[1].text(
            0.5, 0.6, f"{avg_heart_rate:.1f} bpm",
            fontsize=36, ha="center", va="center", fontweight="bold", color="red"
        )
        axes[1].text(
            0.5, 0.4, f"for {min_steps} to {max_steps} steps",
            fontsize=14, ha="center", va="center", fontweight="medium", color="black"
        )

    plt.tight_layout()
    plt.show()

def plot_sleep_min_to_active_min(data: pd.DataFrame, axs: plt.Axes, week_period: str):
    """Helper function to plot one of the regressions in compare_sleep_to_active_min_relationship_for_week_periods()."""
    x, y, regression_line = fit_regression(data, "TotalSleepMin", "TotalActiveMin")

    axs.scatter(x, y, color="green", label="Observations")
    axs.plot(x, regression_line, color="green", label="Regression Line")
    axs.set_xlabel("Sleep Minutes")
    axs.set_ylabel("Active Minutes")
    axs.set_title(f"Regression of Sleep Minutes to Active Minutes on {week_period}")
    axs.legend()
    axs.grid(True)

def fit_regression(data: pd.DataFrame, x_col: str, y_col: str):
    """Helper function to fit a regression to plot."""
    x = data.loc[:, [x_col]].values
    y = data.loc[:, y_col].values
    model = sk.LinearRegression()
    model.fit(x, y)
    regression_line = model.predict(x)

    return x, y, regression_line

def compute_avg_heart_rate(data: pd.DataFrame, min_steps: int, max_steps: int):
    """Helper function to compute the average heart rate for users for given step range."""
    filtered_data = data[
        (data["TotalSteps"] >= min_steps) &
        (data["TotalSteps"] <= max_steps)
    ]
    return filtered_data["AverageHeartRate"].mean()