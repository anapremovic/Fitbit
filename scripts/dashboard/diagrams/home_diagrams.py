from scripts.database import FitbitDatabase

class HomeDiagrams:
    def __init__(self, fitbit_db: FitbitDatabase):
        self.fitbit_db = fitbit_db
