import pandas as pd
import datetime
import numpy as np
from collections import Counter
from zoneinfo import ZoneInfo
import streamlit as st


def filter_fixtures(fixtures: pd.DataFrame) -> pd.DataFrame:
    current_time = datetime.datetime.now(ZoneInfo('Asia/Kolkata'))
    match_finish_times = fixtures['datetime'] + datetime.timedelta(hours=3)
    filtered_fixtures = fixtures[match_finish_times > current_time]
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


def simulate_single_epoch(filtered_fixtures_np: pd.DataFrame, standings: pd.DataFrame, iterations: int = 1000, progress=None) -> pd.DataFrame:
    all_standings = standings[['symbol']].drop(['symbol'], axis=1)
    all_standings[['Q', 'NRR', 'F']] = 0
    for i in range(iterations):
        if progress:
            progress.progress(i/iterations)
        standings = simulate_single_iteration(filtered_fixtures_np, standings)
        all_standings += standings[['Q', 'NRR', 'F']]
    return all_standings * 100/iterations


def simulate_scenarios(filtered_fixtures: pd.DataFrame, standings: pd.DataFrame, iterations: int = 1000, progress=None):
    filtered_fixtures_np = filtered_fixtures.to_numpy()
    standings = standings.sort_values("symbol").reset_index(drop=True)
    all_standings_list = []

    epochs = 10
    for e in range(epochs):
        all_standings = simulate_single_epoch(filtered_fixtures_np, standings, iterations, progress)
        all_standings_list.append(all_standings)

    #
    # all_standings_list
    mean_df = pd.DataFrame(np.array(all_standings_list).mean(axis=0), columns=['Q', 'NRR', 'F'])
    # stdev_df = pd.DataFrame(np.array(all_standings_list).std(axis=0), columns=['QStdev', 'NRRStdev', 'FStdev'])
    final_df = mean_df  # pd.concat([mean_df, stdev_df], axis=1).reset_index(drop=True)
    # final_df['symbol'] = standings['symbol'].reset_index(drop=True)
    final_df = pd.concat([standings[["symbol", "M", "W", "L", "T", "PT"]], mean_df], axis=1)
    final_df = final_df.sort_values('Q', ascending=False) \
        .rename({"symbol": "Team", "Q": "Yes(%)",
                 "M": "Matches", "W": "Wins", "L": "Losses", "T": "Ties", "PT": "Points",
                 "NRR": "On NRR (%)", "F": "No(%)"}, axis=1) \
        .reset_index(drop=True)
    return(final_df)
