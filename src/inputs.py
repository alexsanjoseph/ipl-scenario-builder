import numpy as np
import pandas as pd


def format_standings(current_table: pd.DataFrame) -> pd.DataFrame:
    table_pruned = current_table[['TEAMS', 'M', "W", "L", "T", "PT", "NRR"]][0::2]
    table_pruned['team'] = table_pruned['TEAMS'].str.replace("^\\d*", "", regex=True)
    table_mapping = pd.read_csv("data/team_mappings.csv")
    formatted_table = table_pruned \
        .merge(table_mapping, on='team') \
        .drop(axis=1, columns=['TEAMS', 'team'])
    formatted_table['PT'] = pd.to_numeric(formatted_table['PT'])
    formatted_table['M'] = pd.to_numeric(formatted_table['M'])
    formatted_table['W'] = pd.to_numeric(formatted_table['W'])
    formatted_table['L'] = pd.to_numeric(formatted_table['L'])
    formatted_table['predicted'] = False
    return formatted_table


def get_standings() -> pd.DataFrame:
    print("Getting Current Table")
    TABLE_SOURCE = "https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/points-table-standings"
    all_tables = pd.read_html(TABLE_SOURCE)
    return format_standings(all_tables[0])


def format_fixtures(raw_fixtures: pd.DataFrame) -> pd.DataFrame:
    raw_fixtures.columns = raw_fixtures.iloc[0]
    raw_fixtures = raw_fixtures[1:]
    fixtures_named = raw_fixtures[["Match Centre", "Date", "Time (IST)"]]
    fixtures_named = raw_fixtures.rename({"Match Centre": "match", "Time (IST)": "time"}, axis=1)
    fixtures_named['datetime'] = fixtures_named['Date'] + " " + fixtures_named['time']
    fixtures_named[['for', 'vs', 'against']] = fixtures_named.match.str.split(expand=True)
    fixtures_named['datetime'] = pd.to_datetime(fixtures_named['datetime'])
    fixtures_named.datetime = fixtures_named.datetime.dt.tz_localize('Asia/Kolkata')

    return fixtures_named[['for', 'against', 'datetime']].iloc[:70, :]


def get_fixtures() -> pd.DataFrame:
    TABLE_SOURCE = "https://www.icccricketschedule.com/ipl-2022-schedule-team-venue-time-table-pdf-point-table-ranking-winning-prediction/"
    raw_fixtures = pd.read_html(TABLE_SOURCE)[0]
    # raw_fixtures = pd.read_csv("data/fixtures.csv")
    return format_fixtures(raw_fixtures)


def filter_fixtures(fixtures: pd.DataFrame, standings: pd.DataFrame) -> pd.DataFrame:
    # current_time = datetime.datetime.now(ZoneInfo('Asia/Kolkata'))
    # match_finish_times = fixtures['datetime'] + datetime.timedelta(hours=4)
    total_matches = int(standings['M'].astype(int).sum()/2)  # find total matches done
    filtered_fixtures = fixtures.iloc[total_matches:, ]
    return filtered_fixtures
