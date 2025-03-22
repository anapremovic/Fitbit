import datetime as datetime
import pandas as pd
import plotly.graph_objects as go

class Util:
    @staticmethod
    def filter_by_date_range(df: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Helper function to filter DataFrame by user selected date range from dashboard."""
        return df[(df.loc[:, "Date"] >= start_date) & (df.loc[:, "Date"] <= end_date)]

    @staticmethod
    def filter_by_user(df: pd.DataFrame, user_id: float) -> pd.DataFrame:
        """Helper function to filter DataFrame by user selected user ID from dashboard."""
        return df[(df.loc[:, "UserId"] == user_id)]

    @staticmethod
    def show_no_data_if_empty(df: pd.DataFrame, column_analyzed: str, fig: go.Figure):
        """
        Helper function to check if the relevant data column has data entries available.
        If no entries, overlay "No Data" on top of the corresponding (empty) dashboard figure.
        """
        if df[column_analyzed].dropna().empty:
            fig.add_annotation(
                text="No Data",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=36),
                bgcolor="rgba(0, 0, 0, 0)",
                opacity=0.8
            )

    @staticmethod
    def show_no_data_if_empty_subplot(df: pd.DataFrame, column_analyzed: str,
                                      fig: go.Figure, row: int, col: int):
        """
        Helper function to check if the relevant data column has data entries available.
        If no entries, overlay "No Data" on top of the corresponding (empty) dashboard subplot.
        """
        if df[column_analyzed].dropna().empty:
            fig.add_annotation(
                text="No Data",
                xref="x domain", yref="y domain",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=36),
                bgcolor="rgba(0, 0, 0, 0)",
                opacity=0.8,
                row=row, col=col
            )
