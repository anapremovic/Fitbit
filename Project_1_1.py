import numpy as np
import pandas as pd
from scipy.stats import bernoulli
import matplotlib.pyplot as plt
import os
import seaborn as sns

fitbit = pd.read_csv("data/daily_activity.csv")
users = pd.unique(fitbit['Id'])
print("Total number of users: " + str(len(users)))

data = []
for user in users:
  data.append(fitbit[(fitbit['Id'] == user)]['TotalDistance'].sum())

'''
bins = np.arange(0, max(data) + 5, 15)
plt.hist(data, bins=bins, edgecolor='black')  # Adjust bins for grouping
plt.xlabel("Distance Walked (km)")
plt.ylabel("Frequency")
plt.title("Histogram Plot of Walking Distances")

plt.show()
'''

sns.kdeplot(data, fill=True, color="blue", clip =(0, None), bw_adjust=.5)

plt.xlabel("Distance Walked (km)")
plt.ylabel("Density")
plt.title("Density Plot of Walking Distances")

plt.show()
