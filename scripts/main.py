import pandas as pd
import part1 as part1

# PART 1

daily_activity = pd.read_csv("./data/daily_activity.csv")

part1.generate_day_of_week_frequency_plot(daily_activity)

example_user_id = daily_activity.at[300, 'Id']
part1.generate_regression_line_for_user(daily_activity, example_user_id)
