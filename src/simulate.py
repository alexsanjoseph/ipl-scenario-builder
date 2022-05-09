import pandas as pd
import numpy as np
from collections import Counter
from src.streamlit import add_colour


def simulate_single_iteration(filtered_fixtures_np: pd.DataFrame, standings: pd.DataFrame) -> pd.DataFrame:
    indices = np.random.choice(np.arange(2), len(filtered_fixtures_np), replace=True)
    winner = filtered_fixtures_np[np.arange(filtered_fixtures_np.shape[0]), indices]
    point_counter = Counter(standings['symbol'])
    point_counter.update(winner)
    win_df = pd.DataFrame(point_counter.items(), columns=["symbol", "wins"]) \
        .sort_values(by="symbol")

    standings['final_standings'] = (win_df['wins'] - 1) * 2 + standings['PT']
    t5points_threshold = sorted(standings['final_standings'], reverse=True)[4]
    t4points_threshold = sorted(standings['final_standings'], reverse=True)[3]
    t3points_threshold = sorted(standings['final_standings'], reverse=True)[2]
    t2points_threshold = sorted(standings['final_standings'], reverse=True)[1]

    standings['T2'] = (standings['final_standings'] > t3points_threshold).astype(int)
    standings['T2NRR'] = (standings['final_standings'] == t2points_threshold).astype(int)

    standings['Q'] = (standings['final_standings'] > t5points_threshold).astype(int)
    standings['NRR'] = (standings['final_standings'] == t4points_threshold).astype(int)
    standings['F'] = (standings['final_standings'] < t4points_threshold).astype(int)

    return standings


def simulate_single_epoch(filtered_fixtures_np: pd.DataFrame, standings: pd.DataFrame, iterations: int = 1000, progress=None) -> pd.DataFrame:
    all_standings = standings[['symbol']].drop(['symbol'], axis=1)
    all_standings[['T2', 'T2NRR', 'Q', 'NRR', 'F', "final_standings"]] = 0
    for i in range(iterations):
        if progress:
            progress.progress(i/iterations)
        standings = simulate_single_iteration(filtered_fixtures_np, standings)
        all_standings += standings[['T2', 'T2NRR', 'Q', 'NRR', 'F', 'final_standings']]
    return all_standings * 100/iterations


def simulate_scenarios(filtered_fixtures: pd.DataFrame, standings: pd.DataFrame, iterations: int = 1000, progress=None):
    filtered_fixtures_np = filtered_fixtures.to_numpy()
    standings = standings.sort_values("symbol").reset_index(drop=True)
    all_standings_list = []

    epochs = 1
    for e in range(epochs):
        all_standings = simulate_single_epoch(filtered_fixtures_np, standings, iterations, progress)
        all_standings_list.append(all_standings)

    #
    # all_standings_list
    mean_df = pd.DataFrame(np.array(all_standings_list).mean(axis=0), columns=[
                           'T2', 'T2NRR', 'Q', 'NRR', 'F', "final_standings"])
    # stdev_df = pd.DataFrame(np.array(all_standings_list).std(axis=0), columns=['QStdev', 'NRRStdev', 'FStdev'])
    final_df = mean_df  # pd.concat([mean_df, stdev_df], axis=1).reset_index(drop=True)
    # final_df['symbol'] = standings['symbol'].reset_index(drop=True)
    mean_df['final_standings'] = (mean_df['final_standings'] / 100).round().astype(int)
    final_df = pd.concat([standings[["symbol", "M", "W", "L", "PT"]], mean_df], axis=1)
    final_df = final_df.sort_values(['T2', 'T2NRR', 'Q', 'NRR', "final_standings"], ascending=False) \
        .rename({"symbol": "Team", "Q": "Top 4(%)", "final_standings": "Expected Points",
                 "M": "Matches", "W": "Wins", "L": "Losses", "PT": "Points",
                 "NRR": "Top 4 on NRR (%)", "F": "Not Top 4(%)",
                 'T2': "Top 2", 'T2NRR': "Top 2 on NRR"
                 }, axis=1) \
        .reset_index(drop=True)  \
        .drop("Expected Points", axis=1)
    # .style.applymap(add_colour, subset="Expected Points")
    return(final_df)
