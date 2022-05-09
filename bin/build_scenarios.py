from src.inputs import get_standings, get_fixtures, get_standings, filter_fixtures
from src.simulate import simulate_scenarios
from src.summarize import summarize_results

if __name__ == "__main__":
    fixtures = get_fixtures()
    standings = get_standings()
    filtered_fixtures = filter_fixtures(fixtures, standings)
    all_results = simulate_scenarios(filtered_fixtures, standings)
    print(all_results)
