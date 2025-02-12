import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import datetime as datetime

sns.set_style("darkgrid")

def show_calories_per_day(id: int, start_date: datetime = None, end_date: datetime = None):
  data = pd.read_csv("data/daily_activity.csv")
  get_data_for_id = data.loc[data.loc[:, "Id"] == id].copy()
  get_data_for_id["datetime"] = pd.to_datetime(get_data_for_id.loc[:, "ActivityDate"]) # set up a datetime column
  
  if (start_date == None): start_date = get_data_for_id["datetime"].min()
  if (end_date == None): end_date = get_data_for_id["datetime"].max()
  
  get_data_for_id = get_data_for_id[(get_data_for_id.loc[:, "datetime"] >= start_date) & (get_data_for_id.loc[:, "datetime"] <= end_date)]

  plt.figure(figsize=(12, 6))
  plt.plot(get_data_for_id["datetime"], get_data_for_id["Calories"], marker='o', linestyle="-")
  plt.xlabel("Date of Activity")
  plt.ylabel("Calories Burned")
  plt.title("Calories Burned per Day")
  plt.gca().xaxis.set_major_locator(mdates.DayLocator())  # set ticks for each day
  # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format as YYYY-MM-DD
  
  plt.xticks(rotation = 30)
  plt.show()

show_calories_per_day(6290855005)
# show_calories_per_day(6290855005, datetime.datetime(2016, 4, 3), datetime.datetime(2016, 4, 7)) # only between 2016/4/3 and 2016/4/7
# show_calories_per_day(4020332650)