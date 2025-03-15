import pandas as pd
import datetime as dt
import streamlit as st

class FitbitDatabase:
    def __init__(self, db_location):
        self.db_location = db_location
        self.connection = st.connection("sqlite", type="sql", url=F"sqlite:///{db_location}")

        self.user_ids = self._get_all_user_ids()
        self.min_date, self.max_date = self._get_date_range() # Min and max of our DB's data range

    def _get_all_user_ids(self):
        """Since the result from this function is pretty widely usable, we run it in just once in
        self.__init__ and store the result in self.user_ids for further reference"""

        query = """
            SELECT
                DISTINCT Id
            FROM daily_activity
        """

        df = self.connection.query(query)
        df["Id"] = df["Id"].astype(int)
        return tuple(df.loc[:, "Id"])

    def _get_date_range(self) -> tuple[dt.datetime, dt.datetime]:
        """Since the result from this function is pretty widely usable, we run it in just once in
        self.__init__ and store the result in self.date_range for further reference"""

        query = """
            SELECT DISTINCT ActivityDate AS Date
            FROM daily_activity
        """

        df = self.connection.query(query)
        df["Date"] = pd.to_datetime(df["Date"])

        min_date = df["Date"].min().to_pydatetime()
        max_date = df["Date"].max().to_pydatetime()

        return min_date, max_date

    def get_sleep_moments(self) -> pd.DataFrame:
        query = """
            SELECT 
                Id AS UserId, 
                MAX(SUBSTR(date, 1, INSTR(date, ' ') - 1)) AS Date, 
                COUNT(*) / 60.0 AS SleepHours 
            FROM minute_sleep 
            GROUP BY logId
        """

        df = self.connection.query(query)
        df["Date"] = pd.to_datetime(df["Date"])

        return df

    def get_calories(self) -> pd.DataFrame:
        query = """
            SELECT 
                Id AS UserId, 
                ActivityDate AS Date,
                Calories
            FROM daily_activity;
        """

        df = self.connection.query(query)
        df["Date"] = pd.to_datetime(df["Date"])

        return df

    def get_heart_rate(self):
        query = """
            SELECT 
                Id AS UserId,
                Time AS Date,
                Value AS HeartRate
            FROM heart_rate
        """

        df = self.connection.query(query)
        df["Date"] = pd.to_datetime(df["Date"])

        return df

    def get_intensity(self, user_id: int):
        query = """
            SELECT 
                * 
            FROM hourly_intensity 
            WHERE Id = :id
        """

        return self.connection.query(query, params={"id": user_id})

    def get_daily_activity_for_chicago_comparison(self):
        query = """
            SELECT
                Id,
                ActivityDate,
                TotalDistance,
                Calories
            FROM daily_activity
        """

        return self.connection.query(query)

    def get_active_and_sleep_hrs(self, day_filter: str = "") -> pd.DataFrame:
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

        df = self.connection.query(query)
        df["Date"] = pd.to_datetime(df["Date"])

        if day_filter == "weekdays":
            return df[df["Date"].dt.weekday < 5]
        elif day_filter == "weekends":
            return df[df["Date"].dt.weekday >= 5]

        return df

    def get_sedentary_sleep_activity(self):
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

        df = self.connection.query(query)
        df["Date"] = pd.to_datetime(df["Date"])

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
        
        df = self.connection.query(query)
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
                Id AS UserId,
				substr(ActivityHour, 1, instr(ActivityHour, ' ') - 1) AS Date,
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
            GROUP BY UserId, Date, HourGroup;
        """

        df = self.connection.query(query)

        df["Date"] = pd.to_datetime(df["Date"])

        hour_groups_ordered = ["0-4", "4-8", "8-12", "12-16", "16-20", "20-24"]
        df["HourGroup"] = pd.Categorical(df["HourGroup"], hour_groups_ordered)
        return df.sort_values("HourGroup")

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
				Id AS UserId,
				substr(date, 1, instr(date, ' ') - 1) AS SleepDate,
                COUNT(*) / 60.0 AS HoursSlept,
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
            GROUP BY UserId, SleepDate, HourGroup;
        """

        df = self.connection.query(query)

        df.rename(columns={"SleepDate": "Date"}, inplace=True)
        df["Date"] = pd.to_datetime(df["Date"])

        hour_groups_ordered = ["0-4", "4-8", "8-12", "12-16", "16-20", "20-24"]
        df["HourGroup"] = pd.Categorical(df["HourGroup"], hour_groups_ordered)
        return df.sort_values("HourGroup")
        
    def get_daily_steps(self):
        query = """
            SELECT 
                Id, 
                ActivityDate, 
                TotalSteps 
            FROM daily_activity
        """
        
        return self.connection.query(query)

    def get_hourly_steps(self):
        query = """
            SELECT 
                Id, 
                substr(ActivityHour, 1, instr(ActivityHour, ' ') - 1) AS ActivityDate, 
                StepTotal AS TotalSteps 
            FROM hourly_steps
        """
        
        return self.connection.query(query)

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

        return self.connection.query(query)
