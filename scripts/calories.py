import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as datetime

def show_calories_per_day(data: pd.DataFrame, id: int, start_date: datetime = None, end_date: datetime = None):
  """
  Purpose: This function displays the calories burned for each day given a specific user's ID. Can also set a date range to see a snapshot of the results. Otherwise, the entire duration of calories burned is shown 

  Author: L.D. Lee
  """
  get_data_for_id = data.loc[data.loc[:, "Id"] == id].copy()
  get_data_for_id["datetime"] = pd.to_datetime(get_data_for_id.loc[:, "ActivityDate"]) # Create datetime column
  
  # Set default time ranges
  if (start_date == None): start_date = get_data_for_id["datetime"].min()
  if (end_date == None): end_date = get_data_for_id["datetime"].max()
  
  # Ensure data is in between start and end dates
  get_data_for_id = get_data_for_id[(get_data_for_id.loc[:, "datetime"] >= start_date) & (get_data_for_id.loc[:, "datetime"] <= end_date)]

  # Setup pyplot
  plt.figure(figsize=(12, 8))
  plt.plot(get_data_for_id["datetime"], get_data_for_id["Calories"], marker='o', linestyle="-")
  plt.xlabel("Date of Activity")
  plt.ylabel("Calories Burned")
  plt.title(f"Calories Burned per Day for ID: {id}")
  plt.gca().xaxis.set_major_locator(mdates.DayLocator())  # set ticks for each day
  # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format as YYYY-MM-DD
  
  plt.xticks(rotation = 30)
  plt.show()