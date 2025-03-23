import datetime as datetime
import pandas as pd
import streamlit as st

class FitbitDatabase:
    def __init__(self, db_location):
        self.db_location = db_location
        self.connection = st.connection("sqlite", type="sql", url=F"sqlite:///{db_location}")

        self.user_ids = self._get_all_user_ids()
        self.min_date, self.max_date = self._get_date_range() # Min and max of our DB's data range

    def _query(self, sql_query: str) -> pd.DataFrame:
        """
        Helper function to run a SQL query on our database and ensure
        the Date column is converted to a useful format.
        """

        df = self.connection.query(sql_query, show_spinner=False)
        df["Date"] = pd.to_datetime(df["Date"])
        return df

    def _get_all_user_ids(self) -> tuple[int]:
        """
        Get all user IDs. To be run once on startup and stored in session state.
        """

        query = """
            SELECT
                DISTINCT Id
            FROM daily_activity
        """

        df = self.connection.query(query, show_spinner=False)
        df["Id"] = df["Id"].astype(int)
        return tuple(df.loc[:, "Id"])

    def _get_date_range(self) -> tuple[datetime.datetime, datetime.datetime]:
        """
        Get full date range of dashboard. To be run once on startup and stored in session state.
        """

        query = """
            SELECT DISTINCT ActivityDate AS Date
            FROM daily_activity
        """

        df = self._query(query)

        min_date = df["Date"].min().to_pydatetime()
        max_date = df["Date"].max().to_pydatetime()

        return min_date, max_date

    def get_sleep_durations(self) -> pd.DataFrame:
        """
        Get sleep daily durations in hours.
        """

        query = """
            SELECT 
                Id AS UserId, 
                MAX(SUBSTR(date, 1, INSTR(date, ' ') - 1)) AS Date, 
                COUNT(*) / 60.0 AS SleepHours 
            FROM minute_sleep 
            GROUP BY logId
        """

        df = self._query(query)
        return df

    def get_heart_rate(self, user_id: float) -> pd.DataFrame:
        """
        Get heart rate per day for a given user.
        """

        query = """
            SELECT 
                Id AS UserId,
                Time AS Date,
                Value AS HeartRate
            FROM heart_rate
            WHERE Id = :id
	    """

        df = self.connection.query(query, params={"id": user_id}, show_spinner=False)
        df["Date"] = pd.to_datetime(df.loc[:, "Date"], format = "%m/%d/%Y %I:%M:%S %p")

        return df

    def get_heart_rate_averaged_over_all_users(self) -> pd.DataFrame:
        """
        Get average heart rate over all users for each day.
        """

        query = """
            SELECT 
                SUBSTR(Time, 1, INSTR(Time, ' ') - 1) AS Date,
                AVG(Value) AS HeartRate
            FROM heart_rate
            GROUP BY SUBSTR(Time, 1, INSTR(Time, ' ') - 1)
        """

        df = self._query(query)
        return df

    def get_daily_activity(self) -> pd.DataFrame:
        """
        Get all relevant daily activity data.
        """

        query = """
            SELECT
                Id AS UserId,
                ActivityDate AS Date,
                TotalDistance,
                TotalSteps,
                Calories,
                VeryActiveMinutes,
                FairlyActiveMinutes,
                LightlyActiveMinutes
            FROM daily_activity
        """

        df = self._query(query)
        return df

    def get_active_and_sleep_hrs(self, day_filter: str = "") -> pd.DataFrame:
        """
        Get total active time and sleep duration, in hours, per day.
        Optionally filter by week period: weekdays or weekends only.
        """

        query = """
            SELECT 
                daily_activity.Id AS UserId,
                daily_activity.ActivityDate AS Date,
                SUM(daily_activity.VeryActiveMinutes + daily_activity.FairlyActiveMinutes + daily_activity.LightlyActiveMinutes) / 60.0 AS TotalActiveHours,
                SUM(sleep_moments.SleepMin) / 60.0 AS TotalSleepHours
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

        df = self._query(query)

        if day_filter == "weekdays":
            return df[df["Date"].datetime.weekday < 5]
        elif day_filter == "weekends":
            return df[df["Date"].datetime.weekday >= 5]

        return df

    def get_sedentary_sleep_activity(self) -> pd.DataFrame:
        """
        Get sleep and sedentary duration, in hours, per day.
        """

        query = """
            SELECT 
                minute_sleep.Id AS UserId,
                COUNT(*) / 60.0 AS HoursSlept,
                ActivityDate AS Date, 
                SedentaryMinutes / 60.0 AS SedentaryHours
            FROM minute_sleep 
            INNER JOIN daily_activity 
                ON
                    daily_activity.Id = minute_sleep.Id AND
                    daily_activity.ActivityDate = substr(minute_sleep.date, 1, instr(minute_sleep.date, ' ') - 1)
            GROUP BY logId
        """

        df = self._query(query)
        return df

    def get_daily_step_distribution(self) -> pd.DataFrame:
        """
        Groups the hourly_steps table into 4-hour blocks and returns
        the average amount of steps taken during each block
        """

        query = """
            WITH transformed AS (
                SELECT
                    *,
                    CAST(substr(ActivityHour, instr(ActivityHour, ' ') + 1, instr(ActivityHour, ':') - (instr(ActivityHour, ' ') + 1)) AS INTEGER) AS Hour
                FROM hourly_steps
            )
            SELECT 
                Id AS UserId,
				substr(ActivityHour, 1, instr(ActivityHour, ' ') - 1) AS Date,
                4 * AVG(StepTotal) AS AverageSteps,
                CASE 
                    WHEN ActivityHour LIKE '%AM%'
                        THEN CASE 
                            WHEN (Hour = 12 OR Hour BETWEEN 1 AND 3) THEN '24:00-4:00'
                            WHEN Hour BETWEEN 4 AND 7 THEN '4:00-8:00'
                            WHEN Hour BETWEEN 8 AND 11 THEN '8:00-12:00'
                        END
                    WHEN ActivityHour LIKE '%PM%'
                        THEN CASE
                            WHEN (Hour = 12 OR Hour BETWEEN 1 AND 3) THEN '12:00-16:00'
                            WHEN Hour BETWEEN 4 AND 7 THEN '16:00-20:00'
                            WHEN Hour BETWEEN 8 AND 11 THEN '20:00-24:00'
                        END
                    ELSE 'N/A'
                END AS HourGroup
            FROM transformed
            GROUP BY UserId, Date, HourGroup;
        """

        df = self._query(query)

        hour_groups_ordered = ["24:00-4:00", "4:00-8:00", "8:00-12:00", "12:00-16:00", "16:00-20:00", "20:00-24:00"]
        df["HourGroup"] = pd.Categorical(df["HourGroup"], hour_groups_ordered)
        return df.sort_values("HourGroup")

    def get_daily_calorie_distribution(self) -> pd.DataFrame:
        """
        Groups the hourly_calories table into 4-hour blocks and returns
        the average amount of calories burnt during each block
        """

        query = """
            WITH transformed AS (
                SELECT
                    *,
                    CAST(substr(ActivityHour, instr(ActivityHour, ' ') + 1, instr(ActivityHour, ':') - (instr(ActivityHour, ' ') + 1)) AS INTEGER) AS Hour
                FROM hourly_calories
            )
            SELECT 
                Id AS UserId,
				substr(ActivityHour, 1, instr(ActivityHour, ' ') - 1) AS Date,
				4 * AVG(Calories) AS AverageCalories,
                CASE 
                    WHEN ActivityHour LIKE '%AM%'
                        THEN CASE 
                            WHEN (Hour = 12 OR Hour BETWEEN 1 AND 3) THEN '24:00-4:00'
                            WHEN Hour BETWEEN 4 AND 7 THEN '4:00-8:00'
                            WHEN Hour BETWEEN 8 AND 11 THEN '8:00-12:00'
                        END
                    WHEN ActivityHour LIKE '%PM%'
                        THEN CASE
                            WHEN (Hour = 12 OR Hour BETWEEN 1 AND 3) THEN '12:00-16:00'
                            WHEN Hour BETWEEN 4 AND 7 THEN '16:00-20:00'
                            WHEN Hour BETWEEN 8 AND 11 THEN '20:00-24:00'
                        END
                    ELSE 'N/A'
                END AS HourGroup
            FROM transformed
            GROUP BY UserId, Date, HourGroup;
        """

        df = self._query(query)

        hour_groups_ordered = ["24:00-4:00", "4:00-8:00", "8:00-12:00", "12:00-16:00", "16:00-20:00", "20:00-24:00"]
        df["HourGroup"] = pd.Categorical(df["HourGroup"], hour_groups_ordered)
        return df.sort_values("HourGroup")

    def get_daily_sleep_distribution(self) -> pd.DataFrame:
        """
        Groups the minute_sleep table into 4-hour blocks and returns
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
				Id AS UserId,
				substr(date, 1, instr(date, ' ') - 1) AS SleepDate,
                COUNT(*) / 60.0 AS HoursSlept,
                CASE 
                    WHEN date LIKE '%AM%'
                        THEN CASE 
                            WHEN (Hour BETWEEN 1 AND 3 OR Hour = 12) THEN '24:00-4:00'
                            WHEN Hour BETWEEN 4 AND 7 THEN '4:00-8:00'
                            WHEN Hour BETWEEN 8 AND 11 THEN '8:00-12:00'
                        END
                    WHEN date LIKE '%PM%'
                        THEN CASE
                            WHEN (Hour BETWEEN 1 AND 3 OR Hour = 12) THEN '12:00-16:00'
                            WHEN Hour BETWEEN 4 AND 7 THEN '16:00-20:00'
                            WHEN Hour BETWEEN 8 AND 11 THEN '20:00-24:00'
                        END
                    ELSE 'N/A'
                END AS HourGroup
            FROM transformed
            GROUP BY UserId, SleepDate, HourGroup;
        """

        df = self.connection.query(query, show_spinner=False)

        df.rename(columns={"SleepDate": "Date"}, inplace=True)
        df["Date"] = pd.to_datetime(df.loc[:, "Date"])

        hour_groups_ordered = ["24:00-4:00", "4:00-8:00", "8:00-12:00", "12:00-16:00", "16:00-20:00", "20:00-24:00"]
        df["HourGroup"] = pd.Categorical(df["HourGroup"], hour_groups_ordered)
        return df.sort_values("HourGroup")

    def get_daily_steps_and_average_heart_rate(self) -> pd.DataFrame:
        """
        Get total number of steps and average heart rate, per day.
        """

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

        df = self._query(query)
        return df

    def get_weight_data(self) -> pd.DataFrame:
        """
        Get weight, in kilograms, and BMI per day.
        """

        query = """
        SELECT 
            Id AS UserId,
            substr(Date, 1, instr(Date, ' ') - 1) AS Date,
            WeightKg AS Weight,
            WeightPounds,
            BMI
        FROM weight_log"""

        df = self._query(query)
        df.loc[df.loc[:, "Weight"].isnull(), "Weight"] = df.loc[df.loc[:, "Weight"].isnull(), "WeightPounds"] / 2.205
        df = df.drop(columns=["WeightPounds"])

        return df
    
    def get_activity_grouped_by_user(self) -> pd.DataFrame:
        """
        Get average over all dates for steps, calories, and total active minutes for each user.
        """

        query = """
            SELECT
                Id AS UserId,
                AVG(TotalSteps) AS AverageSteps,
                AVG(Calories) AS AverageCalories,
                AVG(VeryActiveMinutes + FairlyActiveMinutes + LightlyActiveMinutes) AS AverageActiveMinutes
            FROM daily_activity
            GROUP BY Id
        """

        df = self.connection.query(query, show_spinner=False)

        df["UserId"] = pd.Categorical(df["UserId"], categories=df["UserId"])

        return df
