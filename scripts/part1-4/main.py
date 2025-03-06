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

db_location = os.path.join(project_root, "data/fitbit_database.db")
fitbit_database = FitbitDatabase(db_location)

part1 = p1.Part1(project_root)
part1.execute_part_1()

part3 = p3.Part3(fitbit_database, project_root=project_root)
part3.execute_part_3()

part4 = p4.Part4(fitbit_database)
part4.execute_part_4()
