import plotly.graph_objects as go
import plotly.express as px

from scripts.database import FitbitDatabase
from scripts.utils.style import Colors, Fonts

class HomeDiagrams:
    INDICATOR_HEIGHT = 170

    def __init__(self, fitbit_db: FitbitDatabase):
        self.fitbit_db = fitbit_db

    def get_number_of_days(self) -> go.Figure:
        """
        Create an indicator diagram that displays the number of days over
        which the survey took place.
        """

        duration_days = (self.fitbit_db.max_date - self.fitbit_db.min_date).days
        fig = go.Figure(go.Indicator(
            mode="number",
            value=duration_days,
            title={"text": "Surveyed Period", "font": {"size": Fonts.MEDIUM_FONT_SIZE}},
            number={"font": {"size": Fonts.LARGE_FONT_SIZE, "color": Colors.PRIMARY_COLOR}, "suffix": " days"}
        ))

        fig.update_layout(height=self.INDICATOR_HEIGHT, margin=dict(l=0, r=0, t=40, b=0))

        return fig

    def get_number_of_participants(self) -> go.Figure:
        """
        Create an indicator diagram that displays the number of survey participants.
        """

        fig = go.Figure(go.Indicator(
            mode="number",
            value=len(self.fitbit_db.user_ids),
            title={
                "text": "Number of<br>Participants",
                "font": {"size": Fonts.MEDIUM_FONT_SIZE}
            },
            number={"font": {"size": Fonts.LARGE_FONT_SIZE, "color": Colors.PRIMARY_COLOR}}
        ))

        fig.update_layout(height=self.INDICATOR_HEIGHT, margin=dict(l=0, r=0, t=40, b=0))

        return fig

    def get_collective_metrics(self) -> tuple[go.Figure, go.Figure, go.Figure]:
        """
        Create 3 indicator diagrams that display, respectively, the collective number of
        steps taken, distance travelled and minutes spent being active among all participants.
        """

        daily_activity = self.fitbit_db.get_daily_activity()
        collective_active_minutes = (
                daily_activity.loc[:, "VeryActiveMinutes"] +
                daily_activity.loc[:, "FairlyActiveMinutes"] +
                daily_activity.loc[:, "LightlyActiveMinutes"]
        ).sum()
        collective_active_days = collective_active_minutes / 60 // 24
        collective_steps = daily_activity.loc[:, "TotalSteps"].sum()
        collective_distance = round(daily_activity.loc[:, "TotalDistance"].sum(), -2)
        
        active_min_fig = go.Figure(go.Indicator(
            mode="number",
            value=collective_active_days,
            title={
                "text": "Collective Time<br>Spent Exercising",
                "font": {"size": Fonts.MEDIUM_FONT_SIZE}
            },
            number={"font": {"size": Fonts.LARGE_FONT_SIZE, "color": Colors.PRIMARY_COLOR}, "suffix": " days"}
        ))

        steps_fig = go.Figure(go.Indicator(
            mode="number",
            value=collective_steps,
            title={
                "text": "Collective<br>Steps Taken",
                "font": {"size": Fonts.MEDIUM_FONT_SIZE}
            },
            number={"font": {"size": Fonts.LARGE_FONT_SIZE, "color": Colors.PRIMARY_COLOR}}
        ))

        distance_fig = go.Figure(go.Indicator(
            mode="number",
            value=collective_distance,
            title={
                "text": "Collective<br>Distance Walked",
                "font": {"size": Fonts.MEDIUM_FONT_SIZE}
            },
            number={"font": {"size": Fonts.LARGE_FONT_SIZE, "color": Colors.PRIMARY_COLOR}, "suffix": "km"}
        ))

        active_min_fig.update_layout(height=self.INDICATOR_HEIGHT, margin=dict(l=0, r=0, t=40, b=0))
        steps_fig.update_layout(height=self.INDICATOR_HEIGHT, margin=dict(l=0, r=0, t=40, b=0))
        distance_fig.update_layout(height=self.INDICATOR_HEIGHT, margin=dict(l=0, r=0, t=40, b=0))

        return active_min_fig, steps_fig, distance_fig

    def get_steps_distance_active_barplots(self) -> tuple[go.Figure, go.Figure, go.Figure]:
        """
        Create 3 bar plots which display, respectively, the average number of daily steps, 
        the average distance walked and the average number of daily active minutes for each user. 
        In each diagram, the bars are colored (using the same scale) to indicate the corresponding 
        average caloric expenditure per day
        """

        df = self.fitbit_db.get_activity_grouped_by_user()

        df = df.sort_values(by="AverageSteps", ascending=False)
        steps_fig = px.bar(
            df,
            x="UserId",
            y="AverageSteps",
            title="Average Daily Steps",
            subtitle="Color indicates average caloric expenditure per day",
            labels={
                "UserId": "User", 
                "AverageSteps": "Steps", 
                "AverageCalories": "Calories"
            },
            color="AverageCalories",
            color_continuous_scale=[Colors.SECONDARY_COLOR, Colors.PRIMARY_COLOR],
        )
        steps_fig.update_xaxes(type='category', showticklabels=False)
        steps_fig.update_layout(
            coloraxis_showscale=False, 
            title=dict(
                x=0.55,
                xanchor="center",
            ),
        )

        df = df.sort_values(by="AverageDistance", ascending=False)
        distance_fig = px.bar(
            df, 
            x="UserId", 
            y="AverageDistance",
            title="Average Total Distance",
            subtitle="Color indicates average caloric expenditure per day",
            labels={
                "UserId": "User", 
                "AverageSteps": "Steps", 
                "AverageDistance": "Distance (km)",
            },
            color="AverageCalories",
            color_continuous_scale=[Colors.SECONDARY_COLOR, Colors.PRIMARY_COLOR],
        )
        distance_fig.update_xaxes(type='category', showticklabels=False)
        distance_fig.update_layout(
            coloraxis_showscale=False, 
            title=dict(
                x=0.55,
                xanchor="center",
            ),
        )

        df = df.sort_values(by="AverageActiveMinutes", ascending=False)
        active_min_fig = px.bar(
            df,
            x="UserId",
            y="AverageActiveMinutes",
            title="Average Daily Active Time",
            subtitle="Color indicates average caloric expenditure per day",
            labels={
                "UserId": "User", 
                "AverageActiveMinutes": "Active Minutes", 
                "AverageCalories": "Calories",
            },
            color="AverageCalories",
            color_continuous_scale=[Colors.SECONDARY_COLOR, Colors.PRIMARY_COLOR],
        )
        active_min_fig.update_xaxes(type='category', showticklabels=False)
        active_min_fig.update_layout(
            title=dict(
                x=0.55,
                xanchor="center",
            ),
        )

        return (steps_fig, distance_fig, active_min_fig)
