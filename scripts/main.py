import pandas as pd
import calories as ca
import datetime as datetime

# Read from CSV file
data = pd.read_csv("../data/daily_activity.csv")

# Test function calls
ca.show_calories_per_day(data, 6290855005)
ca.show_calories_per_day(data, 6290855005, datetime.datetime(2016, 4, 3), datetime.datetime(2016, 4, 7)) # only between 2016/4/3 and 2016/4/7
ca.show_calories_per_day(data, 4020332650)