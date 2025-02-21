import database as database
import pandas as pd

def verify_correctness(daily_data: pd.DataFrame, hourly_data: pd.DataFrame):
    daily_data_2 = hourly_data.groupby(['Id', 'ActivityDate'], as_index=False).sum()

    # Find common (Id, Date) pairs in both DataFrames
    common_keys = daily_data.loc[:, ['Id', 'ActivityDate']].merge(daily_data_2.loc[:, ['Id', 'ActivityDate']], how='inner')

    # Filter both DataFrames to keep only rows with common (Id, Date) pairs
    df1_common = daily_data.merge(common_keys, on=['Id', 'ActivityDate'])
    df2_common = daily_data_2.merge(common_keys, on=['Id', 'ActivityDate'])

    # Sort by Id and Date
    df1_common_sorted = df1_common.sort_values(by=['Id', 'ActivityDate']).reset_index(drop=True)
    df2_common_sorted = df2_common.sort_values(by=['Id', 'ActivityDate']).reset_index(drop=True)

    print('Is the data correct? ' + str(df1_common_sorted.equals(df2_common_sorted)))

    #Identify for rows with differences
    differences = df1_common_sorted.compare(df2_common_sorted)
    
    #Use conflict indexes to create a new conflicting_data DataFrame
    conflicting_data = df1_common_sorted.loc[differences.index, ['Id', 'ActivityDate']]
    conflicting_data['HourlySteps'] = df1_common_sorted.loc[differences.index, ['TotalSteps']]
    conflicting_data['DailySteps'] = df2_common_sorted.loc[differences.index, ['TotalSteps']]

    # Print the specific users and dates where conflicts occur
    print('Conflicts found for the following users and dates:')
    print(conflicting_data)
 

verify_correctness(database.get_daily_steps(), database.get_hourly_steps())