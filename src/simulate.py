import pandas as pd
import datetime
import numpy as np
from collections import Counter
from zoneinfo import ZoneInfo


def filter_fixtures(fixtures: pd.DataFrame) -> pd.DataFrame:
    current_time = datetime.datetime.now(ZoneInfo('Asia/Kolkata'))
    filtered_fixtures = fixtures[fixtures['datetime'] > current_time].drop(['datetime'], axis=1)
    return filtered_fixtures


def simulate_single_iteration(filtered_fixtures_np: pd.DataFrame, standings: pd.DataFrame) -> pd.DataFrame:
    indices = np.random.choice(np.arange(2), len(filtered_fixtures_np), replace=True)
    winner = filtered_fixtures_np[np.arange(filtered_fixtures_np.shape[0]), indices]
    point_counter = Counter(standings['symbol'])
    point_counter.update(winner)
    win_df = pd.DataFrame(point_counter.items(), columns=["symbol", "wins"]) \
        .sort_values(by="symbol")

    standings['final_standings'] = (win_df['wins'] - 1) * 2 + standings['PT']
    points_threshold = sorted(standings['final_standings'], reverse=True)[5]
    standings['Q'] = (standings['final_standings'] > points_threshold).astype(int)
    standings['NRR'] = (standings['final_standings'] == points_threshold).astype(int)
    standings['F'] = (standings['final_standings'] < points_threshold).astype(int)
    return standings


def simulate_single_epoch(filtered_fixtures_np: pd.DataFrame, standings: pd.DataFrame) -> pd.DataFrame:
    iterations = 100
    all_standings = standings[['symbol']].drop(['symbol'], axis=1)
    all_standings[['Q', 'NRR', 'F']] = 0
    for i in range(iterations):
        standings = simulate_single_iteration(filtered_fixtures_np, standings)
        all_standings += standings[['Q', 'NRR', 'F']]
    return all_standings * 100/iterations


def simulate_scenarios(filtered_fixtures: pd.DataFrame, standings: pd.DataFrame):
    print(filtered_fixtures)
    filtered_fixtures_np = filtered_fixtures.to_numpy()
    standings = standings.sort_values("symbol").reset_index(drop=True)
    all_standings_list = []

    epochs = 10
    # np.random.seed(42)
    for e in range(epochs):
        print(e)
        all_standings = simulate_single_epoch(filtered_fixtures_np, standings)
        all_standings_list.append(all_standings)

    #
    # all_standings_list
    mean_df = pd.DataFrame(np.array(all_standings_list).mean(axis=0), columns=['Q', 'NRR', 'F'])
    # stdev_df = pd.DataFrame(np.array(all_standings_list).std(axis=0), columns=['QStdev', 'NRRStdev', 'FStdev'])
    final_df = mean_df  # pd.concat([mean_df, stdev_df], axis=1).reset_index(drop=True)
    final_df['symbol'] = standings['symbol'].reset_index(drop=True)
    final_df = final_df.sort_values('Q', ascending=False)\
        .rename({"symbol": "team"}) \
        .reset_index(drop=True)
    return(final_df)
