import pandas as pd
import part1 as part1
import calories as ca
import datetime as datetime

# PART 1
daily_activity = pd.read_csv("../data/daily_activity.csv", index_col=0)

ca.show_calories_per_day(daily_activity, 6290855005)
ca.show_calories_per_day(daily_activity, 6290855005, datetime.datetime(2016, 4, 3), datetime.datetime(2016, 4, 7)) # only between 2016/4/3 and 2016/4/7
ca.show_calories_per_day(daily_activity, 4020332650)

part1.generate_day_of_week_frequency_plot(daily_activity)
