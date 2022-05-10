from textwrap import indent
import pandas as pd


def write_output_in_ipl_scenario_format(filtered_fixtures, standings) -> None:
    standings.columns = standings.columns.str.lower()
    standings = standings.rename(columns={"t": "nr", "pt": "p"})
    transposed_standings = standings.set_index("symbol").T
    transposed_standings.columns = transposed_standings.columns.str.lower()
    print("writing standings to file")
    transposed_standings.to_json("standings.json", indent=2)

    filtered_fixtures_write = filtered_fixtures \
        .assign(t1=filtered_fixtures['for'].str.lower(), t2=filtered_fixtures['against'].str.lower()) \
        .assign(win="") \
        .drop(["datetime", "for", "against"], axis=1) \
        .T
    filtered_fixtures_write.to_json("fixtures.json", indent=2)
    print("writing fixtures to file")
