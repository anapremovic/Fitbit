import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
import sqlite3
import datetime
import numpy as np

def heart_rate(id: int, start_date: datetime = None, end_date: datetime = None):
    # Connect to database
    conn = sqlite3.connect("../data/fitbit_database.db")
    heart_rate_db = pd.read_sql(f"SELECT * FROM heart_rate WHERE Id={id}", conn)
    hourly_intensity_db = pd.read_sql(f"SELECT * FROM hourly_intensity WHERE Id={id}", conn)
    
    # Convert columns to datetime
    heart_rate_db["Time"] = pd.to_datetime(heart_rate_db["Time"])
    hourly_intensity_db["ActivityHour"] = pd.to_datetime(hourly_intensity_db["ActivityHour"])

    # Filter data within start and end date
    heart_rate_db = heart_rate_db[(heart_rate_db["Time"] >= start_date) & (heart_rate_db["Time"] <= end_date)]
    hourly_intensity_db = hourly_intensity_db[(hourly_intensity_db["ActivityHour"] >= start_date) & (hourly_intensity_db["ActivityHour"] <= end_date)]

    # Compute averages
    avg_heart_rate = heart_rate_db["Value"].mean()  # Assuming heart rate values are in "Value" column
    avg_intensity = hourly_intensity_db["TotalIntensity"].mean()  # Assuming intensity values are in "Intensity" column

    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Plot Heart Rate over Time
    axes[0, 0].plot(heart_rate_db["Time"], heart_rate_db["Value"], color='red', label='Heart Rate')
    axes[0, 0].set_title("Heart Rate Over Time")
    axes[0, 0].set_xlabel("Time")
    axes[0, 0].set_ylabel("Heart Rate (bpm)")
    axes[0, 0].legend()

    # Plot Hourly Intensity over Time
    axes[0, 1].plot(hourly_intensity_db["ActivityHour"], hourly_intensity_db["TotalIntensity"], color='blue', label='Intensity')
    axes[0, 1].set_title("Hourly Intensity Over Time")
    axes[0, 1].set_xlabel("Time")
    axes[0, 1].set_ylabel("Intensity")
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
    conn = sqlite3.connect("../data/fitbit_database.db")
    daily_activity_db = pd.read_sql("SELECT * FROM daily_activity", conn)
    # daily_activity_db["ActivityDate"] = daily_activity_db["ActivityDate"].astype("time")

    # print(daily_activity_db["ActivityDate"].max())
    # print(daily_activity_db["ActivityDate"].min())
    chicago_data = pd.read_csv("../data/chicago_data.csv")
    
    print(chicago_data["temp"])
    print(chicago_data["precip"])