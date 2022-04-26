from ipaddress import summarize_address_range
from src.inputs import get_current_table, get_fixtures
from src.simulate import simulate_scenarios
from src.summarize import summarize_results
from src.outputs import write_output

if __name__ == "__main__":
    fixtures = get_fixtures()
    current_table = get_current_table()
    all_results = simulate_scenarios(fixtures, current_table)
    results_summary = summarize_results(all_results)
    write_output(results_summary)
