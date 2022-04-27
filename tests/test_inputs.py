import pandas as pd
from src.inputs import format_standings, format_fixtures


def test_format_standings():
    raw_table = pd.read_csv("tests/data/raw_standings.csv")
    expected_output = pd.read_csv("tests/data/expected_standings.csv")
    actual_output = format_standings(raw_table)
    assert all(expected_output == actual_output)


# def test_format_fixtures():
#     raw_fixtures = pd.read_csv("tests/data/raw_fixtures.csv")
#     expected_output = pd.read_csv("tests/data/expected_fixtures.csv")
#     actual_output = format_fixtures(raw_fixtures)
#     assert all(expected_output[['for', 'against']] == actual_output[['for', 'against']])
