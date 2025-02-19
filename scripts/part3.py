import database as db

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

def regression_sedentary_vs_sleep():
    sedentary_data = db.get_all_sedentary_activity()
    sleep_data = db.get_all_sleep_activity()
    sedentary_data = sedentary_data.rename(columns={'ActivityDate': 'date'})
    combined_data = pd.merge(sedentary_data, sleep_data, on=['Id', 'date'])

regression_sedentary_vs_sleep()
