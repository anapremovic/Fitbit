import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as datetime
import database as db
import sklearn.linear_model as sk
import pandas as pd
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_location = os.path.join(project_root, "data/chicago_data.csv")


def execute_part_3():
    """Generate all visualizations for part 3 of the project."""
    verify_correctness(db.get_daily_steps(), db.get_hourly_steps())
    generate_sleep_data_over_time_line_plot(6962181067)
    generate_active_min_to_sleep_min_regression(datetime.datetime(2016, 4, 1))
    display_heart_rate_and_intensity(2022484408)
    display_heart_rate_and_intensity(2022484408, datetime.datetime(2016, 4, 3), datetime.datetime(2016, 4, 7))
    display_weather_correlation_for_chicago()

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


def display_heart_rate_and_intensity(id: int, start_date: datetime = None, end_date: datetime = None):
    """
    Purpose: This function gets a given user's heart rate and hourly intensity, and plots it on a graph. The average heart rate and intensity are also shown

    Author: L.D. Lee
    """
    
    # Connect to database
    heart_rate_db = db.query_database("SELECT * FROM heart_rate WHERE Id = ?", (id,))
    hourly_intensity_db = db.query_database("SELECT * FROM hourly_intensity WHERE Id = ?", (id,))
    
    # Convert Time to datetime with the correct format
    heart_rate_db["Time"] = pd.to_datetime(heart_rate_db["Time"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
    hourly_intensity_db["ActivityHour"] = pd.to_datetime(hourly_intensity_db["ActivityHour"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")

    # Set default time ranges if None
    if start_date is None: start_date = heart_rate_db["Time"].min()
    if end_date is None: end_date = heart_rate_db["Time"].max()

    # Filter data within start and end date
    heart_rate_db = heart_rate_db[(heart_rate_db["Time"] >= start_date) & (heart_rate_db["Time"] <= end_date)]

    # Ensure Time is set as index before resampling
    heart_rate_db.set_index("Time", inplace=True)

    # Resample heart rate data by hour
    heart_rate_hourly = heart_rate_db.resample('h').max()

    # Compute averages
    avg_heart_rate = heart_rate_hourly["Value"].mean()  # Assuming heart rate values are in "Value" column
    avg_intensity = hourly_intensity_db["TotalIntensity"].mean()  # Assuming intensity values are in "Intensity" column

    # Create subplots
    _, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Plot Heart Rate over Time
    axes[0, 0].plot(heart_rate_hourly.index, heart_rate_hourly["Value"], color='red', label='Heart Rate')
    axes[0, 0].set_title("Heart Rate Over Time")
    axes[0, 0].set_xlabel("Time")
    axes[0, 0].set_ylabel("Heart Rate (bpm)")
    axes[0, 0].tick_params(labelrotation=45)
    axes[0, 0].legend()

    # Plot Hourly Intensity over Time
    axes[0, 1].plot(hourly_intensity_db["ActivityHour"], hourly_intensity_db["TotalIntensity"], color='blue', label='Intensity')
    axes[0, 1].set_title("Hourly Intensity Over Time")
    axes[0, 1].set_xlabel("Time")
    axes[0, 1].set_ylabel("Intensity")
    axes[0, 1].tick_params(labelrotation=45)
    axes[0, 1].legend()

    # Display Average Heart Rate
    axes[1, 0].text(0.5, 0.7, "Avg Heart Rate", fontsize=18, ha='center', va='center', fontweight='bold')
    axes[1, 0].text(0.5, 0.4, f"{avg_heart_rate:.2f} bpm", fontsize=40, ha='center', va='center', color='red')
    axes[1, 0].axis("off")

    # Display Average Intensity
    axes[1, 1].text(0.5, 0.7, "Avg Intensity", fontsize=18, ha='center', va='center', fontweight='bold')
    axes[1, 1].text(0.5, 0.4, f"{avg_intensity:.2f}", fontsize=40, ha='center', va='center', color='blue')
    axes[1, 1].axis("off")

    # Adjust layout
    plt.tight_layout()
    plt.show()

def display_weather_correlation_for_chicago():
    """
    Purpose: Displays weather data for the city of Chicago and creates a relationship between the variables
    
    Author: L.D. Lee
    """
    # Connect to database and load Fitbit data
    daily_activity_db = db.query_database("SELECT Id, ActivityDate, TotalDistance, Calories FROM daily_activity")
    daily_activity_db["ActivityDate"] = pd.to_datetime(daily_activity_db["ActivityDate"])

    # Aggregate TotalDistance and Calories per day
    activity_agg = daily_activity_db.groupby("ActivityDate").agg(
        TotalDistance=("TotalDistance", "sum"),
        Calories=("Calories", "sum")
    ).reset_index()

    # Load Chicago weather data
    chicago_data = pd.read_csv(file_location)
    chicago_data["datetime"] = pd.to_datetime(chicago_data["datetime"])

    # Merge Fitbit and weather data
    merged_data = activity_agg.merge(chicago_data, left_on="ActivityDate", right_on="datetime")

    # Compute Correlations
    corr_temp_distance = merged_data["TotalDistance"].corr(merged_data["temp"])
    corr_precip_distance = merged_data["TotalDistance"].corr(merged_data["precip"])
    corr_temp_calories = merged_data["Calories"].corr(merged_data["temp"])
    corr_precip_calories = merged_data["Calories"].corr(merged_data["precip"])

    # Create subplots for visualizations
    _, axes = plt.subplots(2, 2, figsize=(12, 12))

    # Scatter Plot: Temperature vs. Total Distance
    sns.regplot(x=merged_data["temp"], y=merged_data["TotalDistance"], ax=axes[0, 0], color="red")
    axes[0, 0].set_title(f"Temperature vs. Total Distance (Corr: {corr_temp_distance:.3f})")
    axes[0, 0].set_xlabel("Temperature (°C)")
    axes[0, 0].set_ylabel("Total Distance (km)")

    # Scatter Plot: Precipitation vs. Total Distance
    sns.regplot(x=merged_data["precip"], y=merged_data["TotalDistance"], ax=axes[0, 1], color="blue")
    axes[0, 1].set_title(f"Precipitation vs. Total Distance (Corr: {corr_precip_distance:.3f})")
    axes[0, 1].set_xlabel("Precipitation (mm)")
    axes[0, 1].set_ylabel("Total Distance (km)")

    # Scatter Plot: Temperature vs. Calories Burned
    sns.regplot(x=merged_data["temp"], y=merged_data["Calories"], ax=axes[1, 0], color="orange")
    axes[1, 0].set_title(f"Temperature vs. Calories Burned (Corr: {corr_temp_calories:.3f})")
    axes[1, 0].set_xlabel("Temperature (°C)")
    axes[1, 0].set_ylabel("Calories Burned")

    # Scatter Plot: Precipitation vs. Calories Burned
    sns.regplot(x=merged_data["precip"], y=merged_data["Calories"], ax=axes[1, 1], color="green")
    axes[1, 1].set_title(f"Precipitation vs. Calories Burned (Corr: {corr_precip_calories:.3f})")
    axes[1, 1].set_xlabel("Precipitation (mm)")
    axes[1, 1].set_ylabel("Calories Burned")

    plt.tight_layout()
    plt.show()