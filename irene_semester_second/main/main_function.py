import json
from main.pwd_first_solution import run_first_solution, benchmark_first_solution
from main.pwd_second_solution import run_second_solution, benchmark_second_solution

if __name__ == "__main__":
    FILE_PATH = 'rates.json'

    with open(FILE_PATH, 'r') as f:
        my_rate_specs = json.load(f)

    # run first solution and create diagrams
    run_first_solution(
        rate_specs=my_rate_specs, field="pulse", field_value=56, target_field="heart_rate",
        path_to_save='plots/first_solution')

    # # BENCHMARK First Solution
    # benchmark_first_solution(rate_specs=my_rate_specs, field="pulse", field_value=56, target_field="heart_rate",
    #                          path_to_save='plots/first_solution')
    #
    # # run first solution and create diagrams
    # run_second_solution(
    #     rate_specs=my_rate_specs, field="pulse", field_value=56, target_field="heart_rate",
    #     path_to_save='plots/second_solution')
    #
    # # BENCHMARK First Solution
    # benchmark_second_solution(rate_specs=my_rate_specs, field="pulse", field_value=56, target_field="heart_rate",
    #                           path_to_save='plots/second_solution')