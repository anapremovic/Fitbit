import pandas as pd
import part1 as part1
import part3 as p3
import datetime as datetime
import os

# PART 1
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_location = os.path.join(project_root, "data/daily_activity.csv")
daily_activity = pd.read_csv(file_location)

# print("The total number of users is: " + str(part1.calc_num_users(daily_activity)))
# part1.generate_density_plot(daily_activity)
# part1.generate_distance_histogram(daily_activity)

# part1.show_calories_per_day(daily_activity, 6290855005)
# part1.show_calories_per_day(daily_activity, 6290855005, datetime.datetime(2016, 4, 3), datetime.datetime(2016, 4, 7)) # only between 2016/4/3 and 2016/4/7
# part1.show_calories_per_day(daily_activity, 4020332650)

# part1.generate_day_of_week_frequency_plot(daily_activity)

# part1.generate_regression_line_for_user(daily_activity, 5553957443)

p3.heart_rate(2022484408, datetime.datetime(2016, 4, 3), datetime.datetime(2016, 4, 7))
# p3.weather(id = 4020332650)