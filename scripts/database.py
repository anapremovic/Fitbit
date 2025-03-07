import sqlite3
import datetime
import pandas as pd

class FitbitDatabase:
    def __init__(self, db_location):
        self.connection = sqlite3.connect(db_location)
        self.cursor = self.connection.cursor()

    def dataframe_from_query(self, query, parameters = ()):
        """Executes query and returns DataFrame with named columns"""

        self.cursor.execute(query, parameters)
        rows = self.cursor.fetchall()
        return pd.DataFrame(rows, columns = [x[0] for x in self.cursor.description])
    
    @staticmethod
    def get_date_range(df: pd.DataFrame, start_date: datetime, end_date: datetime, column_name: str) -> pd.DataFrame:
        """Helper function to set default start and end dates."""
        if start_date is None:
            start_date = df[column_name].min()
        if end_date is None:
            end_date = df[column_name].max()

        return df[(df.loc[:, column_name] >= start_date) & (df.loc[:, column_name] <= end_date)]

    def get_data_for_given_user_id(self, user_id: int, start_date: datetime = None, end_date: datetime = None) -> pd.DataFrame:
        query = "SELECT * FROM daily_activity WHERE Id = ?"
        df = self.dataframe_from_query(query, (user_id,))
        df["ActivityDate"] = pd.to_datetime(df["ActivityDate"])
        
        # Use helper function to get the date range
        df = self.get_date_range(df, start_date, end_date, "ActivityDate")
        
        return df

    def get_all_user_ids(self):
        query = """
            SELECT
                DISTINCT Id
            FROM daily_activity
        """

        df = self.dataframe_from_query(query)
        df["Id"] = df["Id"].astype(int)
        return df

    def get_sleep_moments(self, user_id: float, start_date: datetime = None, end_date: datetime = None) -> pd.DataFrame:
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

        df = self.dataframe_from_query(query, (user_id,))
        df["Date"] = pd.to_datetime(df["Date"])
        
        # Use helper function to get the date range
        df = self.get_date_range(df, start_date, end_date, "Date")

        return df

    def get_heart_rate(self, user_id: int, start_date: datetime = None, end_date: datetime = None):
        query = """
            SELECT 
                * 
            FROM heart_rate 
            WHERE Id = ?
        """
        heart_rate_db = self.dataframe_from_query(query, (user_id,))
        
        # Convert Time to datetime with the correct format
        heart_rate_db["Time"] = pd.to_datetime(heart_rate_db["Time"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")

        # Use helper function to get the date range
        heart_rate_db = self.get_date_range(heart_rate_db, start_date, end_date, "Time")

        return heart_rate_db

    def get_intensity(self, user_id: int, start_date: datetime = None, end_date: datetime = None):
        query = """
            SELECT 
                * 
            FROM hourly_intensity 
            WHERE Id = ?
        """
        hourly_intensity_db = self.dataframe_from_query(query, (user_id,))
        hourly_intensity_db["ActivityHour"] = pd.to_datetime(hourly_intensity_db["ActivityHour"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
        hourly_intensity_db = self.get_date_range(hourly_intensity_db, start_date, end_date, "ActivityHour")

        return hourly_intensity_db

    def get_daily_activity_for_chicago_comparison(self):
        query = """
            SELECT
                Id,
                ActivityDate,
                TotalDistance,
                Calories
            FROM daily_activity
        """

        return self.dataframe_from_query(query)

    def get_active_and_sleep_min(self, day_filter: str = "") -> pd.DataFrame:
        query = """
            SELECT 
                daily_activity.Id AS UserId,
                daily_activity.ActivityDate AS Date,
                SUM(daily_activity.VeryActiveMinutes + daily_activity.FairlyActiveMinutes + daily_activity.LightlyActiveMinutes) AS TotalActiveMin,
                SUM(sleep_moments.SleepMin) AS TotalSleepMin
            FROM daily_activity
            INNER JOIN (
                SELECT
                    Id AS UserId, 
                    MAX(SUBSTR(date, 1, INSTR(date, ' ') - 1)) AS Date,
                    COUNT(*) AS SleepMin
                FROM minute_sleep
                GROUP BY logId
            ) sleep_moments
            ON
                daily_activity.Id = sleep_moments.UserId 
                AND daily_activity.ActivityDate = sleep_moments.Date
            GROUP BY daily_activity.Id, daily_activity.ActivityDate
        """

        df = self.dataframe_from_query(query)
        df["Date"] = pd.to_datetime(df["Date"])

        if day_filter == "weekdays":
            return df[df["Date"].dt.weekday < 5]
        elif day_filter == "weekends":
            return df[df["Date"].dt.weekday >= 5]

        return df

    def get_sedentary_sleep_activity(self):
        query = """
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
        
        df = self.dataframe_from_query(query)
        df['Id'] = df['Id'].astype(int)
        return df

    def get_daily_step_distribution(self) -> pd.DataFrame:
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
        
        df = self.dataframe_from_query(query)
        hour_groups_ordered = ['0-4', '4-8', '8-12', '12-16', '16-20', '20-24']
        df['HourGroup'] = pd.Categorical(df['HourGroup'], hour_groups_ordered)
        return df.sort_values('HourGroup')

    def get_daily_calorie_distribution(self) -> pd.DataFrame:
        """Groups the hourly_calories table into 4-hour blocks and returns 
        the average amount of calories burnt during each block"""

        query = """
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

        df = self.dataframe_from_query(query)
        hour_groups_ordered = ['0-4', '4-8', '8-12', '12-16', '16-20', '20-24']
        df['HourGroup'] = pd.Categorical(df['HourGroup'], hour_groups_ordered)
        return df.sort_values('HourGroup')

    def get_daily_sleep_distribution(self) -> pd.DataFrame:
        """Groups the minute_sleep table into 4-hour blocks and returns 
        the average amount of minutes slept during each block. Here, we
        take 'average' to mean the total number of minutes slept in an hour
        block divided by the total number of distinct sleep sessions recorded.
        """

        query = """
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

        df = self.dataframe_from_query(query)
        hour_groups_ordered = ['0-4', '4-8', '8-12', '12-16', '16-20', '20-24']
        df['HourGroup'] = pd.Categorical(df['HourGroup'], hour_groups_ordered)

        query  = """
            SELECT
                COUNT(DISTINCT logId) AS NumDistinctSleepSessions 
            FROM minute_sleep
        """

        df2 = self.dataframe_from_query(query)
        num_distinct_sleep_sessions = df2.at[0, 'NumDistinctSleepSessions']

        df.loc[:, 'AverageMinutesSlept'] = df.loc[:, 'TotalMinutesSlept'] / num_distinct_sleep_sessions
        return df.sort_values('HourGroup')
        
    def get_daily_steps(self):
        query = """
            SELECT 
                Id, 
                ActivityDate, 
                TotalSteps 
            FROM daily_activity
        """
        
        return self.dataframe_from_query(query)

    def get_hourly_steps(self):
        query = """
            SELECT 
                Id, 
                substr(ActivityHour, 1, instr(ActivityHour, ' ') - 1) AS ActivityDate, 
                StepTotal AS TotalSteps 
            FROM hourly_steps
        """
        
        return self.dataframe_from_query(query)

    def get_daily_steps_and_average_heart_rate(self) -> pd.DataFrame:
        query = """
            SELECT 
                average_heart_rate.UserId, 
                average_heart_rate.Date, 
                average_heart_rate.AverageHeartRate, 
                daily_activity.TotalSteps
            FROM daily_activity
            INNER JOIN (
                SELECT 
                    Id AS UserId, 
                    substr(Time, 1, instr(Time, ' ') - 1) AS Date, 
                    AVG(value) AS AverageHeartRate
                FROM heart_rate
                GROUP BY Id, substr(Time, 1, instr(Time, ' ') - 1)
            ) average_heart_rate
            ON
                daily_activity.Id = average_heart_rate.UserId AND
                daily_activity.ActivityDate = average_heart_rate.Date
        """

        return self.dataframe_from_query(query)
