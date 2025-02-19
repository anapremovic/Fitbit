import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sqlite3
import datetime
import requests

def heart_rate(id: int, start_date: datetime = None, end_date: datetime = None):
    conn = sqlite3.connect("../data/fitbit_database.db")
    heart_rate_db = pd.read_sql(f"SELECT * FROM heart_rate WHERE Id={id}", conn)
    hourly_intensity_db = pd.read_sql(f"SELECT * FROM hourly_intensity WHERE Id={id}", conn)

    print(heart_rate_db)
    print(hourly_intensity_db)
    # plt.figure(figsize=(12, 8))
    # plt.plot(heart_rate_db["Time"], heart_rate_db["Value"], marker='o', linestyle="-")
    # plt.xlabel("Date of Activity")
    # plt.ylabel("Calories Burned")
    # plt.title(f"Calories Burned per Day for ID: {id}")
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator())  # set ticks for each day
    # plt.show()

def weather():
    conn = sqlite3.connect("../data/fitbit_database.db")
    daily_activity_db = pd.read_sql("SELECT * FROM daily_activity", conn)
    # daily_activity_db["ActivityDate"] = daily_activity_db["ActivityDate"].astype("time")

    # print(daily_activity_db["ActivityDate"].max())
    # print(daily_activity_db["ActivityDate"].min())
    chicago_data = pd.read_csv("../data/chicago_data.csv")
    
    print(chicago_data["temp"])
    print(chicago_data["precip"])