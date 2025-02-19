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
    cursor.execute('SELECT Id, ActivityDate, SedentaryMinutes FROM daily_activity')

    sedentary_data = dataframe_from_cursor_contents()
    sedentary_data.loc[:, 'Id'].astype(int)
    sedentary_data.loc[:, 'ActivityDate'] = pd.to_datetime(sedentary_data.loc[:, 'ActivityDate'])
    return sedentary_data

def get_all_sleep_activity() -> pd.DataFrame:
    cursor.execute(f"SELECT logId, substr(date, 1, instr(date, ' ') - 1) AS date, Id," 
                   f"COUNT(*) AS minutesSlept FROM minute_sleep GROUP BY logId")
    
    sleep_data = dataframe_from_cursor_contents()
    sleep_data.loc[:, 'Id'] = sleep_data.loc[:, 'Id'].astype(int)
    sleep_data.loc[:, 'minutesSlept'] = sleep_data.loc[:, 'minutesSlept'].astype(int)
    sleep_data.loc[:, 'date'] = pd.to_datetime(sleep_data.loc[:, 'date'])
    return sleep_data
