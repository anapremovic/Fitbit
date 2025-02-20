import sqlite3
import os
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_location = os.path.join(project_root, "data/fitbit_database.db")
connection = sqlite3.connect(file_location)
cursor = connection.cursor()

def dataframe_from_cursor_contents():
    """After a query has been executed, this function may be called to obtain a
    DataFrame with named columns from the current contents of the cursor."""
    rows = cursor.fetchall()
    return pd.DataFrame(rows, columns = [x[0] for x in cursor.description])

def get_all_sedentary_activity() -> pd.DataFrame:
    query = """
        SELECT 
            Id, 
            ActivityDate, 
            SedentaryMinutes 
        FROM daily_activity
    """
    cursor.execute('SELECT Id, ActivityDate, SedentaryMinutes FROM daily_activity')

    sedentary_data = dataframe_from_cursor_contents()
    sedentary_data['Id'] = sedentary_data['Id'].astype(int)
    sedentary_data['ActivityDate'] = pd.to_datetime(sedentary_data['ActivityDate'])
    return sedentary_data

def get_all_sleep_activity() -> pd.DataFrame:
    query = """
        SELECT 
            logId, 
            substr(date, 1, instr(date, ' ') - 1) AS date, 
            Id,
            COUNT(*) AS minutesSlept 
        FROM minute_sleep 
        GROUP BY logId
    """
    cursor.execute(query)
    
    # For reassigning a column to an altered version of itself, using .loc is apparently 
    # unreliable since pandas might update a copied version of the column instead of the 
    # original column. And in this case, the code actually breaks using .loc.
    # This is stupid but means [] type of indexing must be used here. According 
    # to ChatGPT, it is still recommended to use .loc in other scenarios. 
    sleep_data = dataframe_from_cursor_contents()
    sleep_data['Id'] = sleep_data['Id'].astype(int)
    sleep_data['minutesSlept'] = sleep_data['minutesSlept'].astype(int)
    sleep_data['date'] = pd.to_datetime(sleep_data['date'])
    return sleep_data

def get_hourly_step_activity() -> pd.DataFrame:
    hour = "CAST(substr(ActivityHour, instr(ActivityHour, ' ') + 1, instr(ActivityHour, ':') - instr(ActivityHour, ' ') - 1) AS INTEGER)"
    query = f"""
        SELECT 
            StepTotal,
        CASE 
            WHEN ActivityHour LIKE '%PM%' AND {hour} < 12 
                THEN {hour} + 12
            WHEN ActivityHour LIKE '%AM%' AND {hour} = 12 
                THEN 0
            ELSE {hour}
        END AS Hour
        FROM hourly_steps;
    """
    cursor.execute(query)

    hourly_step_data = dataframe_from_cursor_contents()

    print(hourly_step_data.dtypes)
    return hourly_step_data

def get_sedentary_vs_sleep_activity() -> pd.DataFrame:
    cursor.execute('SELECT ActivityDate, Id, ')

    df = dataframe_from_cursor_contents()

