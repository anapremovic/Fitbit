import pandas as pd
import datetime as datetime
import os
import part1 as part1
import part3 as part3

# PART 1
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_location = os.path.join(project_root, "data/daily_activity.csv")
daily_activity = pd.read_csv(file_location)

print("The total number of users is: " + str(part1.calc_num_users(daily_activity)))
part1.generate_distance_walked_density_plot(daily_activity)
part1.generate_distance_histogram(daily_activity)

part1.generate_calories_burned_line_graph(daily_activity, 6290855005)
part1.generate_calories_burned_line_graph(daily_activity, 6290855005, datetime.datetime(2016, 4, 3), datetime.datetime(2016, 4, 7)) # only between 2016/4/3 and 2016/4/7
part1.generate_calories_burned_line_graph(daily_activity, 4020332650)

part1.generate_day_of_week_frequency_plot(daily_activity)

part1.generate_steps_to_calories_regression(daily_activity, 5553957443)

# PART 3
part3.generate_active_min_to_sleep_min_regression(datetime.datetime(2016, 4, 1))
part3.generate_sleep_data_over_time_line_plot(6962181067)
