import sqlite3
import os
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_location = os.path.join(project_root, "data/fitbit_database.db")
connection = sqlite3.connect(file_location)
cursor = connection.cursor()

def get_active_min_data() -> pd.DataFrame:
    query = """
    SELECT Id AS UserId, 
            ActivityDate AS Date, 
            SUM(VeryActiveMinutes + FairlyActiveMinutes + LightlyActiveMinutes) AS TotalActiveMin
    FROM daily_activity
    GROUP BY Id, ActivityDate
    ORDER By Id, ActivityDate;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    active_min_data = pd.DataFrame(rows, columns=[x[0] for x in cursor.description])
    active_min_data["Date"] = pd.to_datetime(active_min_data.loc[:, "Date"])
    return active_min_data

def get_sleep_data():
    query = """
    SELECT logId AS LogId, 
           MAX(date) AS Date, 
           Id AS UserId, 
           COUNT(*) AS MinSlept
    FROM minute_sleep 
    GROUP BY logId;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    sleep_data = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    sleep_data["Date"] = pd.to_datetime(sleep_data.loc[:, "Date"])
    return sleep_data
