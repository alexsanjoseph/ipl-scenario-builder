from src.inputs import get_standings, get_fixtures, get_standings
from src.simulate import simulate_scenarios
from src.summarize import summarize_results
from src.outputs import write_output

if __name__ == "__main__":
    fixtures = get_fixtures()
    standings = get_standings()
    print(standings)
    all_results = simulate_scenarios(fixtures, standings)
    results_summary = summarize_results(all_results)
    write_output(results_summary)
