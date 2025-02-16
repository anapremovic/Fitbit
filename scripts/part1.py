import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import seaborn as sns


def generate_day_of_week_frequency_plot(daily_activity: DataFrame):
    daily_activity["ActivityDate"] = pd.to_datetime(daily_activity.loc[:, "ActivityDate"])
    day_of_week_counts = daily_activity.loc[:, "ActivityDate"].dt.dayofweek.value_counts().sort_index()

    plt.figure(figsize=(8, 5))
    plt.bar(day_of_week_counts.index, day_of_week_counts.values, color="green")
    plt.xticks(ticks=range(7), labels=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    plt.ylabel("Frequency")
    plt.title("Total Number of Workouts Per Day of Week")
    plt.show()

def generate_regression_line_for_user(daily_activity: DataFrame, user_id: str):
    user_entries = daily_activity.loc[ daily_activity.loc[:, 'Id'] == user_id ]
    user_steps = user_entries.loc[:, 'TotalSteps']
    user_calories = user_entries.loc[:, 'Calories']

    plt.scatter(user_steps, user_calories, color="green", label='Observations')

    least_squares_model = smf.ols(formula='Calories ~ TotalSteps + C(Id)', data=daily_activity).fit()
    base_intercept = least_squares_model.params["Intercept"]
    steps_coef = least_squares_model.params["TotalSteps"]
    user_coef = least_squares_model.params.get(f'C(Id)[T.{user_id}]', 0)

    y_intercept = (0, base_intercept + user_coef)
    plt.axline(y_intercept, slope=steps_coef, color="green", label='Regression line')

    plt.title(f'Scatter plot of Steps Taken vs. Calories Burned for ID: {user_id}')
    plt.xlabel('Total steps')
    plt.ylabel('Calories burned')
    plt.grid()
    plt.legend()
    plt.show()

def calc_num_users(data: pd.DataFrame,):
  """Calculates the total number of unique users in the dataset"""
  users = pd.unique(data.loc[:,'Id'])
  return len(users)

def visualize_data(data: pd.DataFrame,):
  """Create a density plot of the total distance walked by individuals"""
  users = pd.unique(data.loc[:,'Id'])
  distances = []
  for user in users:
    distances.append(data.loc[data.loc[:,'Id'] == user, 'TotalDistance'].sum())
  
  #Clip the data at 0 as there are no users walking less than 0 kilometers
  #Reduce the bandwidth to prevent smoothing and create a more representative plot
  sns.kdeplot(distances, fill=True, color="blue", clip =(0, None), bw_adjust=1)

  plt.xlabel("Distance Walked (km)")
  plt.ylabel("Density")
  plt.title("Density Plot of Walking Distances")

  plt.show()
  
def histogram_visualization(data: pd.DataFrame,):
  """Create a histogram describing the frequency
    of the total number of steps walked by individuals"""
  users = pd.unique(data.loc[:,'Id'])
  distances = []
  for user in users:
    distances.append(data.loc[data.loc[:,'Id'] == user, 'TotalDistance'].sum())
  bins = np.arange(0, max(distances), 15)
  plt.hist(distances, bins=bins, edgecolor='black') 
  plt.xticks(bins)
  plt.xlim(min(bins), max(bins))
  plt.xlabel("Distance Walked (km)")
  plt.ylabel("Frequency")
  plt.title("Histogram Plot of Walking Distances")

  plt.show()