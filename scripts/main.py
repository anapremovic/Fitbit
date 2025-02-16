import pandas as pd
import part1 as part1
import calories as ca
import datetime as datetime
import os

# PART 1
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_location = os.path.join(project_root, "data/daily_activity.csv")
daily_activity = pd.read_csv(file_location)

print("The total number of users is: " + str(part1.calc_num_users(daily_activity)))
part1.visualize_data(daily_activity)

ca.show_calories_per_day(daily_activity, 6290855005)
ca.show_calories_per_day(daily_activity, 6290855005, datetime.datetime(2016, 4, 3), datetime.datetime(2016, 4, 7)) # only between 2016/4/3 and 2016/4/7
ca.show_calories_per_day(daily_activity, 4020332650)

part1.generate_day_of_week_frequency_plot(daily_activity)

example_user_id = daily_activity.at[300, 'Id']
part1.generate_regression_line_for_user(daily_activity, example_user_id)

