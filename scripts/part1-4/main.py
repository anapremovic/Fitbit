# ----------
# Add project root to PATH to simplify relative imports
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
sys.path.append(project_root)
# ----------

import part1 as p1
import part3 as p3
import part4 as p4
from scripts.database import FitbitDatabase

# Part 1
activity_csv = os.path.join(project_root, "data/daily_activity.csv")
part1 = p1.Part1(activity_csv)
part1.execute_part_1()

db_location = os.path.join(project_root, "data/fitbit_database.db")
fitbit_database = FitbitDatabase(db_location)

# Part 3
weather_csv = os.path.join(project_root, "data/chicago_data.csv")
part3 = p3.Part3(fitbit_database, weather_csv)
part3.execute_part_3()

# Part 4
part4 = p4.Part4(fitbit_database)
part4.execute_part_4()
