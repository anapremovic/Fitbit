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
    def get_no_data_figure(title: str):
        fig = go.Figure()
        fig.add_annotation(
            text="No Data",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=36)
        )
        fig.update_layout(title=title, xaxis=dict(visible=False), yaxis=dict(visible=False))

        return fig
