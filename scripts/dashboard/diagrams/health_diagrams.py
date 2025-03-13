def plot_calories_burned(data, user_id: int, start_date: datetime = None, end_date: datetime = None):
    """
    Purpose: This function displays the calories burned for each day given a specific user's ID. 
    Can also set a date range to see a snapshot of the results. Otherwise, the entire duration of calories burned is shown 
    """
    data_for_id = data.loc[data.loc[:, "Id"] == user_id ].copy()
    data_for_id["datetime"] = pd.to_datetime(data_for_id.loc[:,"ActivityDate"], errors="coerce") # Create datetime column
    # Set default time ranges
    if start_date is None:
        start_date = data_for_id["datetime"].min()
    if end_date is None:
        end_date = data_for_id["datetime"].max()
    # Ensure data is in between start and end dates
    data_for_id = data_for_id[
        (data_for_id.loc[:,"datetime"] >= start_date) & 
        (data_for_id.loc[:,"datetime"] <= end_date)
    ]

    # Setup pyplot
    plt.figure(figsize=(12, 8))
    plt.plot(data_for_id["datetime"], data_for_id["Calories"], marker='o', linestyle="-")
    plt.xlabel("Date of Activity")
    plt.ylabel("Calories Burned")
    plt.title(f"Calories Burned per Day for ID: {user_id}")
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())  # set ticks for each day

    plt.xticks(rotation = 30)
    return plt

def plot_weight_change_vs_steps(weight_data, step_data, user_id: int):
    """Generates a plot of weight change vs daily steps for a given user"""
    weight_data = weight_data.loc[user_id, ['Weight']]
    
    # Reindex step_data to be by date for a particular user
    step_data = step_data.loc[step_data.loc[:, 'Id'] == user_id].set_index('ActivityDate').loc[:, ['TotalSteps']]

    # Reindex weight_data to match step_data and forward-fill missing values
    df = weight_data.reindex(step_data.index).ffill()

    # Join TotalSteps from step_data to df
    df = df.join(step_data, how='left')

    
    # Plot weight change vs. daily steps
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x=df["TotalSteps"], y=df["Weight"], edgecolor='black')

    plt.xlabel("Steps per Day")
    plt.ylabel("Weight (kg)")
    plt.title(f"Weight vs. Daily Steps for User {user_id}")
    plt.grid(True)
    return plt