import database as db
import numpy as np
import datetime as datetime
import seaborn as sns
import scipy.stats as sp
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import sklearn.linear_model as sk
import pandas as pd
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_location = os.path.join(project_root, "data/chicago_data.csv")

def execute_part_3():
    """Generate all visualizations for part 3 of the project."""
    verify_correctness(db.get_daily_steps(), db.get_hourly_steps())
    generate_sleep_data_over_time_line_plot(6962181067)
    generate_sleep_min_to_active_min_regression()
    display_heart_rate_and_intensity(2022484408)
    display_heart_rate_and_intensity(2022484408, datetime.datetime(2016, 4, 3), datetime.datetime(2016, 4, 7))
    display_weather_correlation_for_chicago()
    generate_sedentary_min_to_sleep_min_regression()
    generate_daily_step_distribution_barplot()
    generate_daily_calorie_distribution_barplot()
    generate_daily_sleep_distribution_barplot()

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

def generate_sleep_min_to_active_min_regression():
    """Generates a regression that shows how sleep minutes relate to active minutes for all users and days."""

    active_and_sleep_min_grouped_by_user = db.get_active_and_sleep_min()
    if active_and_sleep_min_grouped_by_user.empty:
        print("No activity and/or sleep data available.")
        return

    x = active_and_sleep_min_grouped_by_user.loc[:, ["TotalSleepMin"]].values
    y = active_and_sleep_min_grouped_by_user.loc[:, "TotalActiveMin"].values
    model = sk.LinearRegression()
    model.fit(x, y)
    regression_line = model.predict(x)

    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, color="green", label="Observations")
    plt.plot(x, regression_line, color="green", label="Regression Line")
    plt.xlabel("Sleep Minutes")
    plt.ylabel("Active Minutes")
    plt.title("Regression of Sleep Minutes to Active Minutes")
    plt.legend()
    plt.grid()
    plt.show()

def display_heart_rate_and_intensity(user_id: int, start_date: datetime = None, end_date: datetime = None):
    """
    Purpose: This function gets a given user's heart rate and hourly intensity, and plots it on a graph. The average heart rate and intensity are also shown

    Author: L.D. Lee
    """
    
    # Connect to database
    heart_rate_db = db.get_heart_rate(user_id)
    hourly_intensity_db = db.get_intensity(user_id)
    
    # Convert Time to datetime with the correct format
    heart_rate_db["Time"] = pd.to_datetime(heart_rate_db["Time"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
    hourly_intensity_db["ActivityHour"] = pd.to_datetime(hourly_intensity_db["ActivityHour"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")

    # Set default time ranges if None
    if start_date is None: start_date = heart_rate_db["Time"].min()
    if end_date is None: end_date = heart_rate_db["Time"].max()

    # Filter data within start and end date
    heart_rate_db = heart_rate_db.loc[(heart_rate_db["Time"] >= start_date) & (heart_rate_db["Time"] <= end_date)]

    # Ensure Time is set as index before resampling
    heart_rate_db.set_index("Time", inplace=True)

    # Resample heart rate data by hour
    heart_rate_hourly = heart_rate_db.resample('h').max().loc[:, ["Value"]]

    # Compute averages
    avg_heart_rate = heart_rate_hourly.loc[:, "Value"].mean()
    avg_intensity = hourly_intensity_db.loc[:, "TotalIntensity"].mean()

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
    daily_activity_db = db.get_daily_activity_for_chicago_comparison()
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
    merged_data = activity_agg.merge(chicago_data, left_on="ActivityDate", right_on="datetime").loc[:, ["TotalDistance", "Calories", "temp", "precip"]]

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

def generate_sedentary_min_to_sleep_min_regression():
    """Analyses the relationship between the amount of sedentary activity and the
    sleep duration for all individuals by performing a linear regression on all
    data with the sleep duration as response variable and the sedentary activity
    as explanatory variables. """

    sedentary_sleep_data = db.get_sedentary_sleep_activity()

    least_squares_model = smf.ols(formula='MinutesSlept ~ SedentaryMinutes', data=sedentary_sleep_data).fit()
    intercept = least_squares_model.params['Intercept']
    slope = least_squares_model.params['SedentaryMinutes']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6), layout='tight')
    ax1.scatter(sedentary_sleep_data.loc[:, 'SedentaryMinutes'], sedentary_sleep_data.loc[:, 'MinutesSlept'], 
                color='C0', label='Observations')
    ax1.axline((0, intercept), slope=slope, color='C0', label='Regression line')
    ax1.set_title('Relation Daily Sedentary Time and Time Slept \n Across All Users')
    ax1.set_xlabel('Sedentary Minutes')
    ax1.set_ylabel('Minutes Slept')
    ax1.legend()

    # Visually verify errors are normally distributed
    residuals = least_squares_model.resid
    root_mse = np.sqrt(np.mean(residuals ** 2))
    residual_range = np.arange(-600, 600, 5)
    norm_pdf = sp.norm.pdf(residual_range, loc=0, scale=root_mse)
    ax2.hist(residuals, bins=20, range=(-600, 600), 
             color='C0', density=True, label='Residuals')
    ax2.plot(residual_range, norm_pdf, color='C1', label=r'$\mathcal{N}(0, \sqrt{MSE})$')
    ax2.set_title('Distribution of Residuals')
    ax2.set_xlabel('Residual')
    ax2.set_ylabel('Density')
    ax2.legend()
    plt.show()

def generate_daily_step_distribution_barplot():
    """Divide a day into 6 4-hour blocks and compute the average amount of steps
    taken per time block across all users. Visualize results in a bar plot."""
    
    step_data = db.get_daily_step_distribution()

    plt.bar(step_data.loc[:, 'HourGroup'], step_data.loc[:, 'AverageSteps'],
            color='C2')
    plt.title('Average Number of Steps Taken per 4-Hour Time Block \n Across All Users')
    plt.xlabel('Time')
    plt.ylabel('Steps Taken')
    plt.show()

def generate_daily_calorie_distribution_barplot():
    """Divide a day into 6 4-hour blocks and compute the average amount of calories
    burnt per time block across all users. Visualize results in a bar plot."""

    calorie_data = db.get_daily_calorie_distribution()

    plt.bar(calorie_data.loc[:, 'HourGroup'], calorie_data.loc[:, 'AverageCalories'],
            color='C3')
    plt.title('Average Number of Calories Burnt per 4-Hour Time Block \n Across All Users')
    plt.xlabel('Time')
    plt.ylabel('Calories Burnt')
    plt.show()

def generate_daily_sleep_distribution_barplot():
    """Divide a day into 6 4-hour blocks and compute the average amount of minutes
    slept per time block across all users. Visualize results in a bar plot."""

    sleep_data = db.get_daily_sleep_distribution()

    plt.bar(sleep_data.loc[:, 'HourGroup'], sleep_data.loc[:, 'AverageMinutesSlept'],
            color='C4')
    plt.title('Average Number of Minutes Slept per 4-Hour Time Block \n Across All Users')
    plt.xlabel('Time')
    plt.ylabel('Minutes Slept')
    plt.show()
