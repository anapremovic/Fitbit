import sqlite3
import os
import pandas as pd
import datetime as datetime

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_location = os.path.join(project_root, "data/fitbit_database.db")
connection = sqlite3.connect(file_location)
cursor = connection.cursor()

def dataframe_from_cursor_contents():
    """After a query has been executed, this function may be called to obtain a
    DataFrame with named columns from the current contents of the cursor."""
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

def get_all_sleep_activity() -> pd.DataFrame:
    query = """
        SELECT 
            logId, 
            substr(date, 1, instr(date, ' ') - 1) AS date, 
            Id,
            COUNT(*) AS minutesSlept 
        FROM minute_sleep 
        GROUP BY logId
    """
    cursor.execute(query)
    
    # For reassigning a column to an altered version of itself, using .loc is apparently 
    # unreliable since pandas might update a copied version of the column instead of the 
    # original column. And in this case, the code actually breaks using .loc.
    # This is stupid but means [] type of indexing must be used here. According 
    # to ChatGPT, it is still recommended to use .loc in other scenarios. 
    df = dataframe_from_cursor_contents()
    df['Id'] = df['Id'].astype(int)
    df['minutesSlept'] = df['minutesSlept'].astype(int)
    df['date'] = pd.to_datetime(df['date'])
    return df

def get_sedentary_sleep_activity():
    query = f"""
        SELECT 
            minute_sleep.Id,
            COUNT(*) AS MinutesSlept,
            ActivityDate AS Date, 
            SedentaryMinutes
        FROM minute_sleep 
        INNER JOIN daily_activity 
            ON
                daily_activity.Id = minute_sleep.Id AND
                daily_activity.ActivityDate = substr(minute_sleep.date, 1, instr(minute_sleep.date, ' ') - 1)
        GROUP BY logId
    """
    cursor.execute(query)

    df = dataframe_from_cursor_contents()
    df['Id'] = df['Id'].astype(int)
    print(df)
    return df

def get_daily_step_distribution() -> pd.DataFrame:
    """Groups the hourly_steps table into 4-hour blocks and returns 
    the average amount of steps taken during each block"""

    query = """
        WITH transformed AS (
            SELECT
                *,
                CAST(substr(ActivityHour, instr(ActivityHour, ' ') + 1, instr(ActivityHour, ':') - (instr(ActivityHour, ' ') + 1)) AS INTEGER) AS Hour
            FROM hourly_steps
        )
        SELECT 
            4 * AVG(StepTotal) AS AverageSteps,
            CASE 
                WHEN ActivityHour LIKE '%AM%'
                    THEN CASE 
                        WHEN (Hour = 12 OR Hour BETWEEN 1 AND 3) THEN '0-4'
                        WHEN Hour BETWEEN 4 AND 7 THEN '4-8'
                        WHEN Hour BETWEEN 8 AND 11 THEN '8-12'
                    END
                WHEN ActivityHour LIKE '%PM%'
                    THEN CASE
                        WHEN (Hour = 12 OR Hour BETWEEN 1 AND 3) THEN '12-16'
                        WHEN Hour BETWEEN 4 AND 7 THEN '16-20'
                        WHEN Hour BETWEEN 8 AND 11 THEN '20-24'
                    END
                ELSE 'N/A'
            END AS HourGroup
        FROM transformed
        GROUP BY HourGroup;
    """
    cursor.execute(query)

    hour_groups_ordered = ['0-4', '4-8', '8-12', '12-16', '16-20', '20-24']
    df = dataframe_from_cursor_contents()
    df['HourGroup'] = pd.Categorical(df['HourGroup'], hour_groups_ordered)
    return df.sort_values('HourGroup')

def get_daily_calorie_distribtion() -> pd.DataFrame:
    """Groups the hourly_calories table into 4-hour blocks and returns 
    the average amount of calories burnt during each block"""

    query = f"""
        WITH transformed AS (
            SELECT
                *,
                CAST(substr(ActivityHour, instr(ActivityHour, ' ') + 1, instr(ActivityHour, ':') - (instr(ActivityHour, ' ') + 1)) AS INTEGER) AS Hour
            FROM hourly_calories
        )
        SELECT 
            4 * AVG(Calories) AS AverageCalories,
            CASE 
                WHEN ActivityHour LIKE '%AM%'
                    THEN CASE 
                        WHEN (Hour = 12 OR Hour BETWEEN 1 AND 3) THEN '0-4'
                        WHEN Hour BETWEEN 4 AND 7 THEN '4-8'
                        WHEN Hour BETWEEN 8 AND 11 THEN '8-12'
                    END
                WHEN ActivityHour LIKE '%PM%'
                    THEN CASE
                        WHEN (Hour = 12 OR Hour BETWEEN 1 AND 3) THEN '12-16'
                        WHEN Hour BETWEEN 4 AND 7 THEN '16-20'
                        WHEN Hour BETWEEN 8 AND 11 THEN '20-24'
                    END
                ELSE 'N/A'
            END AS HourGroup
        FROM transformed
        GROUP BY HourGroup;
    """
    cursor.execute(query)

    hour_groups_ordered = ['0-4', '4-8', '8-12', '12-16', '16-20', '20-24']
    df = dataframe_from_cursor_contents()
    df['HourGroup'] = pd.Categorical(df['HourGroup'], hour_groups_ordered)
    return df.sort_values('HourGroup')

def get_daily_sleep_distribution() -> pd.DataFrame:
    """Groups the minute_sleep table into 4-hour blocks and returns 
    the average amount of minutes slept during each block. Here, we
    take 'average' to mean the total number of minutes slept in an hour
    block divided by the total number of distinct sleep sessions recorded.
    """

    query = f"""
        WITH transformed AS (
            SELECT
                *,
                CAST(substr(date, instr(date, ' ') + 1, instr(date, ':') - (instr(date, ' ') + 1)) AS INTEGER) AS Hour
            FROM minute_sleep
        )
        SELECT 
            COUNT(*) AS TotalMinutesSlept,
            CASE 
                WHEN date LIKE '%AM%'
                    THEN CASE 
                        WHEN (Hour BETWEEN 1 AND 3 OR Hour = 12) THEN '0-4'
                        WHEN Hour BETWEEN 4 AND 7 THEN '4-8'
                        WHEN Hour BETWEEN 8 AND 11 THEN '8-12'
                    END
                WHEN date LIKE '%PM%'
                    THEN CASE
                        WHEN (Hour BETWEEN 1 AND 3 OR Hour = 12) THEN '12-16'
                        WHEN Hour BETWEEN 4 AND 7 THEN '16-20'
                        WHEN Hour BETWEEN 8 AND 11 THEN '20-24'
                    END
                ELSE 'N/A'
            END AS HourGroup
        FROM transformed
        GROUP BY HourGroup;
    """
    cursor.execute(query)

    hour_groups_ordered = ['0-4', '4-8', '8-12', '12-16', '16-20', '20-24']
    df = dataframe_from_cursor_contents()
    df['HourGroup'] = pd.Categorical(df['HourGroup'], hour_groups_ordered)

    cursor.execute('SELECT COUNT(DISTINCT logId) AS NumDistinctSleepSessions FROM minute_sleep')
    numDistinctSleepSessions = dataframe_from_cursor_contents().at[0, 'NumDistinctSleepSessions']

    df.loc[:, 'AverageMinutesSlept'] = df.loc[:, 'TotalMinutesSlept'] / numDistinctSleepSessions
    return df.sort_values('HourGroup')

    return pd.DataFrame(rows, columns = [x[0] for x in cursor.description])

def convert_datetime_to_string(date: datetime) -> str:
    if os.name == "nt":  # Windows
        return date.strftime("%#m/%#d/%Y")
    else:  # macOS/Linux
        return date.strftime("%-m/%-d/%Y")
