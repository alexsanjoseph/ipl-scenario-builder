import pandas as pd
import datetime
import numpy as np
from collections import Counter
from zoneinfo import ZoneInfo


def simulate_scenarios(fixtures: pd.DataFrame, standings: pd.DataFrame):
    current_time = datetime.datetime.now(ZoneInfo('Asia/Kolkata'))
    filtered_fixtures = fixtures[fixtures['datetime'] > current_time].drop(['datetime'], axis=1)
    filtered_fixtures_np = filtered_fixtures.to_numpy()
    standings = standings.sort_values("symbol")
    all_standings_list = []

    epochs = 100
    iterations = 50
    # np.random.seed(42)
    for e in range(epochs):
        print(e)
        all_standings = standings[['symbol']].drop(['symbol'], axis=1)
        all_standings[['Q', 'NRR', 'F']] = 0
        for i in range(iterations):
            indices = np.random.choice(np.arange(2), len(filtered_fixtures), replace=True)
            winner = filtered_fixtures_np[np.arange(len(filtered_fixtures)), indices]
            point_counter = Counter(standings['symbol'])
            point_counter.update(winner)
            win_df = pd.DataFrame(point_counter.items(), columns=["symbol", "wins"]) \
                .sort_values(by="symbol")

            standings['final_standings'] = win_df['wins'] * 2 + standings['PT']
            points_threshold = sorted(standings['final_standings'], reverse=True)[5]
            standings['Q'] = (standings['final_standings'] > points_threshold).astype(int)
            standings['NRR'] = (standings['final_standings'] == points_threshold).astype(int)
            standings['F'] = (standings['final_standings'] < points_threshold).astype(int)
            all_standings += standings[['Q', 'NRR', 'F']]
        all_standings_list.append(all_standings)

    #
    # all_standings_list
    mean_df = pd.DataFrame(np.array(all_standings_list).mean(axis=0) * 100/iterations, columns=['Q', 'NRR', 'F'])
    # stdev_df = pd.DataFrame(np.array(all_standings_list).std(axis=0), columns=['QStdev', 'NRRStdev', 'FStdev'])
    final_df = mean_df  # pd.concat([mean_df, stdev_df], axis=1).reset_index(drop=True)
    final_df['symbol'] = standings['symbol'].reset_index(drop=True)
    final_df = final_df.sort_values('Q', ascending=False)
    print(final_df)
    print("simulating scenarios")
