import plotly.graph_objects as go
import plotly.express as px

from scripts.database import FitbitDatabase

PRIMARY_COLOR = "#06B0B8"
MEDIUM_FONT_SIZE = 25
LARGE_FONT_SIZE = 50

class HomeDiagrams:
    def __init__(self, fitbit_db: FitbitDatabase):
        self.fitbit_db = fitbit_db

    def get_number_of_days(self):
        """Create an indicator diagram that displays the number of days over
        which the survey took place"""

        duration_days = (self.fitbit_db.max_date - self.fitbit_db.min_date).days
        fig = go.Figure(go.Indicator(
            mode="number",
            value=duration_days,
            title={"text": "Days Followed", "font": {"size": MEDIUM_FONT_SIZE, "color": PRIMARY_COLOR}},
            number={"font": {"size": LARGE_FONT_SIZE}}#, "suffix": " days"} # Change color later
        ))

        fig.update_layout(height=150, margin=dict(l=0, r=0, t=0, b=0))

        return fig
    
    def get_number_of_participants(self):
        """Create an indicator diagram that displays the number of survey participants"""

        fig = go.Figure(go.Indicator(
            mode="number",
            value=len(self.fitbit_db.user_ids),
            title={
                "text": "Participants",
                "font": {"size": MEDIUM_FONT_SIZE, "color": PRIMARY_COLOR}
            },
            number={"font": {"size": LARGE_FONT_SIZE}} # Change color later
        ))

        fig.update_layout(height=150, margin=dict(l=0, r=0, t=0, b=0))

        return fig

    def get_collective_metrics(self) -> tuple[go.Figure, go.Figure, go.Figure]:
        """Create 3 indicator diagrams that display, respectively, the collective number of 
        steps taken, distance travelled and minutes spent being active among all participants."""

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
                "font": {"size": MEDIUM_FONT_SIZE, "color": PRIMARY_COLOR}
            },
            number={"font": {"size": LARGE_FONT_SIZE}} # Change color later
        ))

        fig2 = go.Figure(go.Indicator(
            mode="number",
            value=collective_distance,
            title={
                "text": "Distance", 
                "font": {"size": MEDIUM_FONT_SIZE, "color": PRIMARY_COLOR}
            },
            number={"font": {"size": LARGE_FONT_SIZE}, "suffix": "km"} # Change color later
        ))

        fig3 = go.Figure(go.Indicator(
            mode="number",
            value=collective_active_minutes,
            title={
                "text": "Active Minutes", 
                "font": {"size": MEDIUM_FONT_SIZE, "color": PRIMARY_COLOR}
            },
            number={"font": {"size": LARGE_FONT_SIZE}} # Change color later
        ))

        fig1.update_layout(height=150, margin=dict(l=0, r=0, t=0, b=0))
        fig2.update_layout(height=150, margin=dict(l=0, r=0, t=0, b=0))
        fig3.update_layout(height=150, margin=dict(l=0, r=0, t=0, b=0))

        return (fig1, fig2, fig3)

    def get_steps_and_active_barplot(self) -> tuple[go.Figure, go.Figure]:
        """Create 2 bar plots which display, respectively, the average number of daily steps 
        and the average number of daily active minutes for each user. In each diagram, the bars are
        colored (using the same scale) to indicate the corresponding average caloric expenditure 
        per day"""

        df = self.fitbit_db.get_activity_grouped_by_user()

        df = df.sort_values(by="AverageSteps", ascending=False)
        fig1 = px.bar(
            df, 
            x="Id", 
            y="AverageSteps",
            title="Average Daily Steps",
            subtitle="Color indicates average caloric expenditure per day",
            labels={"Id": "User", "AverageSteps": "Steps", "AverageCalories": "Calories"},
            color="AverageCalories",
            color_continuous_scale=["#FFFFFF", "#06B0B8"],
        )
        fig1.update_xaxes(type='category', tickangle=-45, showticklabels=False)
        # Color scale is also given in the next barplot. Since they are same, 
        # we can remove this one
        fig1.update_layout(coloraxis_showscale=False)

        df = df.sort_values(by="AverageActiveMinutes", ascending=False)
        fig2 = px.bar(
            df, 
            x="Id", 
            y="AverageActiveMinutes",
            title="Average Daily Active Time",
            subtitle="Color indicates average caloric expenditure per day",
            labels={"Id": "User", "AverageActiveMinutes": "Active Minutes", "AverageCalories": "Calories"},
            color="AverageCalories",
            color_continuous_scale=["#FFFFFF", "#06B0B8"],
        )
        fig2.update_xaxes(type='category', showticklabels=False)

        return (fig1, fig2)
