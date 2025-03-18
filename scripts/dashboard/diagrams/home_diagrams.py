import plotly.graph_objects as go

from plotly.subplots import make_subplots

from scripts.database import FitbitDatabase


class HomeDiagrams:
    def __init__(self, fitbit_db: FitbitDatabase):
        self.fitbit_db = fitbit_db

    @staticmethod
    def human_format(num):
        num = float(f'{num:.2g}')
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

    def get_total_metrics_row(self):
        num_participants = len(self.fitbit_db.user_ids);

        fig = make_subplots(
            rows=1, cols=4, 
            subplot_titles=[
                "Number of participants",
                "Research Period", # date range with number of days as subscript
                "Collective steps taken",
                "Collective distance travelled",
                "Collective active time",
                "Collective calories burned",
            ], 
            horizontal_spacing=0.2
        )
        
        fig = go.Figure(go.Indicator(
            mode="number",
            value=len(self.fitbit_db.user_ids),
            title={"text": "Total Participants"},
            number={"font": {"size": 60, "color": "white"}} # Change color later
        ))

        return fig
    
    def get_number_of_days(self):
        duration_days = (self.fitbit_db.max_date - self.fitbit_db.min_date).days
        fig = go.Figure(go.Indicator(
            mode="number",
            value=duration_days,
            title={"text": "Days tracked", "font": {"size": 30, "color": "#84C9FF"}},
            number={"font": {"size": 50}}#, "suffix": " days"} # Change color later
        ))

        fig.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0))

        return fig
    
    def get_number_of_participants(self):
        fig = go.Figure(go.Indicator(
            mode="number",
            value=len(self.fitbit_db.user_ids),
            title={"text": "Participants", "font": {"size": 30, "color": "#84C9FF"}},
            number={"font": {"size": 50}} # Change color later
        ))

        fig.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0))

        return fig
    
    def get_collective_steps(self):
        collective_steps_taken = self.fitbit_db.get_daily_steps().loc[:, "TotalSteps"].sum()

        fig = go.Figure(go.Indicator(
            mode="number",
            value=collective_steps_taken,
            title={"text": "Steps", "font": {"size": 30, "color": "#84C9FF"}},
            number={"font": {"size": 50}} # Change color later
        ))

        fig.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0))

        return fig
    
    def get_collective_distance(self):
        collective_steps_taken = self.fitbit_db.get_daily_steps().loc[:, "TotalSteps"].sum()

        fig = go.Figure(go.Indicator(
            mode="number",
            value=collective_steps_taken,
            title={"text": "Steps", "font": {"size": 30, "color": "#84C9FF"}},
            number={"font": {"size": 50}} # Change color later
        ))

        fig.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0))

        return fig
