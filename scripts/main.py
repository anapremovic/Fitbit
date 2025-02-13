import pandas as pd
import part1 as part1

# PART 1

daily_activity = pd.read_csv("../data/daily_activity.csv", index_col=0)

part1.generate_day_of_week_frequency_plot(daily_activity)
