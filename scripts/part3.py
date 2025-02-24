import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import database as db
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_location = os.path.join(project_root, "data/chicago_data.csv")

def heart_rate(id: int, start_date: datetime = None, end_date: datetime = None):
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

def weather():
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