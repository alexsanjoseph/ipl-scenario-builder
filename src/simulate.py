import pandas as pd
import datetime


def simulate_scenarios(fixtures: pd.DataFrame, standings: pd.DataFrame):
    current_date = datetime.datetime.today()
    print("simulating scenarios")
