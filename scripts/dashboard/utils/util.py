import datetime as datetime
import pandas as pd

class Util:
    @staticmethod
    def filter_by_date_range(df: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Helper function to filter DataFrame by user selected date range from dashboard."""
        return df[(df.loc[:, "Date"] >= start_date) & (df.loc[:, "Date"] <= end_date)]

    @staticmethod
    def filter_by_user(df: pd.DataFrame, user_id: float) -> pd.DataFrame:
        """Helper function to filter DataFrame by user selected user ID from dashboard."""
        return df[(df.loc[:, "UserId"] == user_id)]
