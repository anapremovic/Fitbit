import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sqlite3
import datetime

def heart_rate(id: int, start_date: datetime = None, end_date: datetime = None):
    """
    Purpose: This function gets a given user's heart rate and hourly intensity, and plots it on a graph. The average heart rate and intensity are also shown

    Author: L.D. Lee
    """
    
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

    # Aggregate heart rate by hour (sum of all heart rate values per hour)
    heart_rate_hourly = heart_rate_db.resample('H', on='Time').max()

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

def weather(id: int):
    """
    Purpose: Displays weather data for the city of Chicago and creates a relationship between the variables
    
    Author: L.D. Lee
    """
    # Connect to database and load data for all users
    conn = sqlite3.connect("../data/fitbit_database.db")
    daily_activity_db = pd.read_sql("SELECT Id, ActivityDate, TotalDistance FROM daily_activity", conn)

    # Convert 'ActivityDate' to datetime
    daily_activity_db["ActivityDate"] = pd.to_datetime(daily_activity_db["ActivityDate"])

    # Load Chicago weather data
    chicago_data = pd.read_csv("../data/chicago_data.csv")
    chicago_data["datetime"] = pd.to_datetime(chicago_data["datetime"])

    # Create figure and axis
    fig, ax1 = plt.subplots(figsize=(10, 5))
    plt.xticks(rotation=45)  # Rotate x-axis labels for readability

    # First line (Precipitation)
    ax1.plot(chicago_data["datetime"], chicago_data["precip"], 'b-', label="Precipitation")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Precipitation (mm)", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Second Y-axis (Temperature)90
    ax2 = ax1.twinx()
    ax2.plot(chicago_data["datetime"], chicago_data["temp"], 'r-', label="Temperature")
    ax2.set_ylabel("Temperature (°C)", color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Third Y-axis (Total Distance for Multiple Users)
    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 60))  # Offset third y-axis
    ax3.set_ylabel("Total Distance (km)", color='green')

    # Plot totalDistance for each user
    for user_id, user_data in daily_activity_db.groupby("Id"):
        ax3.plot(user_data["ActivityDate"], user_data["TotalDistance"], label=f"User {user_id}", linestyle="--")

    ax3.tick_params(axis='y', labelcolor='green')

    # Formatting
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.tight_layout()
    plt.title("Weather and Total Distance Comparison for Multiple Users")
    plt.legend(loc="upper left")

    plt.show()
