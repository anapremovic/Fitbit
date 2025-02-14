import pandas as pd
import part1 as part1
import os

# PART 1
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_location = os.path.join(project_root, "data/daily_activity.csv")

daily_activity = pd.read_csv(file_location)

part1.generate_day_of_week_frequency_plot(daily_activity)

example_user_id = daily_activity.at[300, 'Id']
part1.generate_regression_line_for_user(daily_activity, example_user_id)
