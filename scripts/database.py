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

def get_daily_step_distribution() -> pd.DataFrame:
    """Requests to group the hourly_steps table into 4-hour blocks and return 
    the average amount of steps for each"""
    # SQLite query to extract just the hour from the ActivityHour column
    hour = "CAST(substr(ActivityHour, instr(ActivityHour, ' ') + 1, instr(ActivityHour, ':') - instr(ActivityHour, ' ') - 1) AS INTEGER)"
    # Returns a column containing the hour blocks (0-4, 4-8, ..., 20-24)
    # for each entry in the table. Then groups table by said blocks and computes
    # the average number of steps taken during each: 4 * [average steps per hour].
    query = f"""
        SELECT 
            4 * AVG(StepTotal) AS AverageSteps
            CASE 
                WHEN ActivityHour LIKE '%AM%'
                    THEN CASE 
                        WHEN ({hour} BETWEEN 1 AND 3 OR {hour} = 12) THEN '0-4'
                        WHEN {hour} BETWEEN 4 AND 7 THEN '4-8'
                        WHEN {hour} BETWEEN 8 AND 11 THEN '8-12'
                    END
                WHEN ActivityHour LIKE '%PM%'
                    THEN CASE
                        WHEN ({hour} BETWEEN 1 AND 3 OR {hour} = 12) THEN '12-16'
                        WHEN {hour} BETWEEN 4 AND 7 THEN '16-20'
                        WHEN {hour} BETWEEN 8 AND 11 THEN '20-24'
                    END
                ELSE 'N/A'
            END AS HourGroup,
        FROM hourly_steps
        GROUP BY HourGroup;
    """
    cursor.execute(query)

    step_data = dataframe_from_cursor_contents()
    sorted_hour_groups = ['0-4', '4-8', '8-12', '12-16', '16-20', '20-24']
    step_data['HourGroup'] = pd.Categorical(step_data['HourGroup'], sorted_hour_groups)
    return step_data.sort_values('HourGroup')

def get_sedentary_vs_sleep_activity() -> pd.DataFrame:
    cursor.execute('SELECT ActivityDate, Id, ')

    df = dataframe_from_cursor_contents()

