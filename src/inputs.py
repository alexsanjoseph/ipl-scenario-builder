import numpy as np
import pandas as pd


def format_standings(current_table: pd.DataFrame) -> pd.DataFrame:
    table_pruned = current_table[['TEAMS', 'M', "W", "L", "T", "PT"]][0::2]
    table_pruned['team'] = table_pruned['TEAMS'].str.replace("^\\d*", "", regex=True)
    table_mapping = pd.read_csv("data/team_mappings.csv")
    formatted_table = table_pruned \
        .merge(table_mapping, on='team') \
        .drop(axis=1, columns=['TEAMS', 'team'])
    formatted_table['PT'] = pd.to_numeric(formatted_table['PT'])
    return formatted_table


def get_standings() -> pd.DataFrame:
    print("Getting Current Table")
    TABLE_SOURCE = "https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/points-table-standings"
    all_tables = pd.read_html(TABLE_SOURCE)
    return format_standings(all_tables[0])


def format_fixtures(raw_fixtures: pd.DataFrame) -> pd.DataFrame:
    fixtures_named = raw_fixtures[["Date", "Match Details"]] \
        .rename({"Match Details": "match", "Date": "date"}, axis=1)
    fixtures_named[['for', 'vs', 'against']] = fixtures_named.match.str.split(expand=True)
    fixtures_named.drop(axis=1, columns=['vs', 'match'], inplace=True)
    fixtures_named['date'] = pd.to_datetime(fixtures_named['date'])
    return fixtures_named


def get_fixtures() -> pd.DataFrame:
    raw_fixtures = pd.read_csv("data/fixtures.csv")
    return format_fixtures(raw_fixtures)
