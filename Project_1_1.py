import numpy as np
import pandas as pd
from scipy.stats import bernoulli
import matplotlib.pyplot as plt
import os
import seaborn as sns

fitbit = pd.read_csv("data/daily_activity.csv")


def calc_num_users(fitbit):
  """Calculates the total number of unique users in the dataset"""
  users = pd.unique(fitbit['Id'])
  return len(users)

def visualize_data(fitbit):
  """Create a density plot of the total distance walked by individuals"""
  users = pd.unique(fitbit['Id'])
  data = []
  for user in users:
    data.append(fitbit[(fitbit['Id'] == user)]['TotalDistance'].sum())
  
  #Clip the data at 0 as there are no users walking less than 0 kilometers
  #Reduce the bandwidth to prevent smoothing and create a more representative plot
  sns.kdeplot(data, fill=True, color="blue", clip =(0, None), bw_adjust=1)

  plt.xlabel("Distance Walked (km)")
  plt.ylabel("Density")
  plt.title("Density Plot of Walking Distances")

  plt.show()
  
def histogram_visualization(fitbit):
  """Create a histogram describing the frequency
    of the total number of steps walked by individuals"""
  users = pd.unique(fitbit['Id'])
  data = []
  for user in users:
    data.append(fitbit[(fitbit['Id'] == user)]['TotalDistance'].sum())
  bins = np.arange(0, max(data), 15)
  plt.hist(data, bins=bins, edgecolor='black') 
  plt.xticks(bins)
  plt.xlim(min(data), max(bins))
  plt.xlabel("Distance Walked (km)")
  plt.ylabel("Frequency")
  plt.title("Histogram Plot of Walking Distances")

  plt.show()

calc_num_users(fitbit)
visualize_data(fitbit)
histogram_visualization(fitbit)