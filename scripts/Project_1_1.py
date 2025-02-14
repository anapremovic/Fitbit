import numpy as np
import pandas as pd
from scipy.stats import bernoulli
import matplotlib.pyplot as plt
import os
import seaborn as sns

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