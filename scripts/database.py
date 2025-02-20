import sqlite3
import os
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_location = os.path.join(project_root, "data/fitbit_database.db")
connection = sqlite3.connect(file_location)
cursor = connection.cursor()


def get_sleep_data():
    query = f"SELECT GROUP_CONCAT(DISTINCT substr(date, 1, instr(date, ' ') - 1)) AS date, Id, COUNT(*) AS minutesSlept FROM minute_sleep GROUP BY logId"
    cursor.execute(query)
    rows = cursor.fetchall()
    sleep_data = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    sleep_data.loc[:, 'Id'] = sleep_data.loc[:, 'Id'].astype(int)
    sleep_data.loc[:, 'minutesSlept'] = sleep_data.loc[:, 'minutesSlept'].astype(int)
    return sleep_data

print(get_sleep_data())