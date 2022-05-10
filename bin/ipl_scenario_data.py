from src.inputs import get_standings, get_fixtures, get_standings, filter_fixtures
from src.outputs import write_output_in_ipl_scenario_format

if __name__ == "__main__":
    fixtures = get_fixtures()
    standings = get_standings()
    filtered_fixtures = filter_fixtures(fixtures, standings)
    write_output_in_ipl_scenario_format(filtered_fixtures, standings)
