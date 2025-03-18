import plotly.graph_objects as go

from scripts.database import FitbitDatabase

PRIMARY_COLOR = "#06B0B8"

class HomeDiagrams:
    def __init__(self, fitbit_db: FitbitDatabase):
        self.fitbit_db = fitbit_db

    def get_number_of_days(self):
        duration_days = (self.fitbit_db.max_date - self.fitbit_db.min_date).days
        fig = go.Figure(go.Indicator(
            mode="number",
            value=duration_days,
            title={"text": "Days tracked", "font": {"size": 30, "color": PRIMARY_COLOR}},
            number={"font": {"size": 50}}#, "suffix": " days"} # Change color later
        ))

        fig.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0))

        return fig
    
    def get_number_of_participants(self):
        fig = go.Figure(go.Indicator(
            mode="number",
            value=len(self.fitbit_db.user_ids),
            title={
                "text": "Participants",
                "font": {"size": 30, "color": PRIMARY_COLOR}
            },
            number={"font": {"size": 50}} # Change color later
        ))

        fig.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0))

        return fig

    def get_collective_metrics(self) -> tuple[go.Figure, go.Figure, go.Figure]:
        daily_activity = self.fitbit_db.get_daily_activity()
        collective_steps = daily_activity.loc[:, "TotalSteps"].sum()
        collective_active_minutes = (
            daily_activity.loc[:, "VeryActiveMinutes"] + 
            daily_activity.loc[:, "FairlyActiveMinutes"] + 
            daily_activity.loc[:, "LightlyActiveMinutes"]
        ).sum()
        collective_distance = round(daily_activity.loc[:, "TotalDistance"].sum(), -2)

        fig1 = go.Figure(go.Indicator(
            mode="number",
            value=collective_steps,
            title={
                "text": "Steps", 
                "font": {"size": 30, "color": PRIMARY_COLOR}
            },
            number={"font": {"size": 50}} # Change color later
        ))

        fig2 = go.Figure(go.Indicator(
            mode="number",
            value=collective_distance,
            title={
                "text": "Distance", 
                "font": {"size": 30, "color": PRIMARY_COLOR}
            },
            number={"font": {"size": 50}, "suffix": "km"} # Change color later
        ))

        fig3 = go.Figure(go.Indicator(
            mode="number",
            value=collective_active_minutes,
            title={
                "text": "Active Minutes", 
                "font": {"size": 30, "color": PRIMARY_COLOR}
            },
            number={"font": {"size": 50}} # Change color later
        ))

        fig1.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0))
        fig2.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0))
        fig3.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0))

        return (fig1, fig2, fig3)

