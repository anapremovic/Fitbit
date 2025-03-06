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

#p1.execute_part_1()
#p3.execute_part_3()
#p4.execute_part_4()
