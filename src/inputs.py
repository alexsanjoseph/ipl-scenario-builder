import pandas as pd


def get_current_table() -> pd.DataFrame:
    print("Getting Current Table")


def get_fixtures() -> pd.DataFrame:
    print("Getting fixtures")
    return pd.read_csv("data/fixtures.csv")[[""]]
