import sqlite3
import os
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_location = os.path.join(project_root, "data/fitbit_database.db")
connection = sqlite3.connect(file_location)
cursor = connection.cursor()

def fetch_total_active_minutes_per_user_and_date() -> pd.DataFrame:
    query = """
    SELECT Id, ActivityDate, SUM(VeryActiveMinutes + FairlyActiveMinutes + LightlyActiveMinutes) AS TotalActiveMinutes
    FROM daily_activity
    GROUP BY Id, ActivityDate
    ORDER By Id, ActivityDate;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    return pd.DataFrame(rows, columns=[x[0] for x in cursor.description])