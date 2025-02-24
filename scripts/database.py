import sqlite3
import os
import pandas as pd
import datetime as datetime

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_location = os.path.join(project_root, "data/fitbit_database.db")
connection = sqlite3.connect(file_location)
cursor = connection.cursor()


def get_sleep_moments(user_id: float) -> pd.DataFrame:
    query = """
    SELECT 
        Id AS UserId, 
        MAX(SUBSTR(date, 1, INSTR(date, ' ') - 1)) AS Date, 
        COUNT(*) AS SleepMin 
    FROM minute_sleep 
    WHERE Id = ?
    GROUP BY logId
    ORDER BY Date;
    """

    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    sleep_moments = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    sleep_moments["Date"] = pd.to_datetime(sleep_moments.loc[:, "Date"])
    return sleep_moments

def get_active_and_sleep_min_grouped_by_user(date: datetime) -> pd.DataFrame:
    query = """
    SELECT 
        daily_activity.Id AS UserId,
        ActivityDate AS Date,
        SUM(daily_activity.VeryActiveMinutes + daily_activity.FairlyActiveMinutes + daily_activity.LightlyActiveMinutes) AS TotalActiveMin,
        SUM(sleep_moments.SleepMin) AS TotalSleepMin
    FROM daily_activity
    INNER JOIN (SELECT
                    Id AS UserId, 
                    MAX(SUBSTR(date, 1, INSTR(date, ' ') - 1)) AS Date,
                    COUNT(*) AS SleepMin
                FROM minute_sleep 
                GROUP BY logId) sleep_moments
        ON
            daily_activity.Id = sleep_moments.UserId AND
            daily_activity.ActivityDate = sleep_moments.Date
    WHERE daily_activity.ActivityDate = ?
    GROUP BY daily_activity.Id;"""

    date_str = convert_datetime_to_string(date)
    cursor.execute(query, (date_str,))
    rows = cursor.fetchall()
    return pd.DataFrame(rows, columns = [x[0] for x in cursor.description])

def convert_datetime_to_string(date: datetime) -> str:
    if os.name == "nt":  # Windows
        return date.strftime("%#m/%#d/%Y")
    else:  # macOS/Linux
        return date.strftime("%-m/%-d/%Y")
    
def get_daily_steps():
    query = f"SELECT Id, ActivityDate, TotalSteps FROM daily_activity"
    cursor.execute(query)
    rows = cursor.fetchall()
    daily_steps = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    return daily_steps

def get_hourly_steps():
    query = f"SELECT Id, substr(ActivityHour, 1, instr(ActivityHour, ' ') - 1) AS ActivityDate, StepTotal AS TotalSteps FROM hourly_steps"
    cursor.execute(query)
    rows = cursor.fetchall()
    hourly_steps = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    return hourly_steps