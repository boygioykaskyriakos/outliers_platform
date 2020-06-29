import time
import random

from collections import Counter

from main.public_functions import create_structured_dict, print_data, \
    linear_search_equals, linear_search_bigger, linear_search_smaller, \
    visualize_results_simple_plot, visualize_results_hist
from main.user_defined_constants import unit, normal, max, min, range_values


def my_health_care_numpy(rates_values_dict: dict, n: int) -> list:
    """
    This function generates a list of dictionaries for n records based on the data specifications

    :param rates_values_dict: dict: dictionary that contains data specifications
    :param n: int: n amount of records
    :return: list of dict: measurements
    """
    # initialize
    temp_dict = {}
    my_array_values = []

    rates_values_dict_copy = rates_values_dict.copy()
    # seed random
    random.seed(109)
    # generate measurements according the data specifications for n records
    # creates a list of dicts
    for records in range(n):
        for key, value in rates_values_dict_copy.items():
            if key == "timestamp":
                temp_dict[key] = records
            else:
                if value[unit] == "int":
                    temp_dict[key] = random.randint(value[range_values][min], value[range_values][max])
                elif value[unit] == "float":
                    temp_dict[key] = \
                        random.randint(value[range_values][min] * 10, value[range_values][max] * 10) / 10

        my_array_values.append(temp_dict.copy())

    return my_array_values


class AnalyticsFirstSolution:
    """
    This class contains all the analytics
    """
    def __init__(self, array_measurements: list, rate_specs: dict):
        """
        Initialize function of class

        :param array_measurements: np.arrray : numpy array containing the measurements
        :param rate_specs: dict: dictionary that contains data specifications
        """
        self.array_values = array_measurements
        self.rate_specs = rate_specs

    def get_sample_array(self, sample_size: int) -> list:
        """
        This method gets a subset from the array_values

        :param sample_size: int : indicates the sample that will be used from the self array
        :return: list: a sample_array based on size
        """

        sample_indexes = random.sample(range(len(self.array_values)), sample_size)
        sample_array = [ele for idx, ele in enumerate(self.array_values) if idx in sample_indexes]

        return sample_array

    def find_abnormal_values(self, field: str, sample_array: list) -> (dict, list):
        """
        This method finds abnormal values on a specific field, given by the user, and returns:
        - a dictionary with the results in a structured visual form
        - a  with the results

        :param sample_array: list : a subset from the array_values
        :param field: str: field to search for abnormal values
        :return: (dict: that contains the results in a structured form, list: contains the results in numpy form)
        """
        # initialize
        visual_results = {}
        plot_array = []

        sub_array = [arr[field] for arr in sample_array]
        d_type = self.rate_specs[field][unit]

        if d_type == "int":
            step = 1
        else:
            step = 0.1
        # get abnormal values from data specifications
        abnormal_values_min = self.rate_specs[field][normal][min] - step
        abnormal_values_max = self.rate_specs[field][normal][max] + step
        # find abnormal values indices
        res_match_min = linear_search_smaller(sub_array, abnormal_values_min)
        res_match_max = linear_search_bigger(sub_array, abnormal_values_max)
        res_match_indices = res_match_min + res_match_max
        # select appropriate data from numpy array
        visual_array = [
            [ele['timestamp'], ele[field]] for idx, ele in enumerate(sample_array) if idx in res_match_indices]

        plot_array.append([ele['timestamp'] for idx, ele in enumerate(sample_array) if idx in res_match_indices])
        plot_array.append([ele[field] for idx, ele in enumerate(sample_array) if idx in res_match_indices])

        # create results
        visual_results["abnormal_{}_count".format(field)] = len(res_match_indices)
        visual_results["abnormal_values"] = visual_array

        return visual_results, plot_array

    def frequency_histogram_first_solution(self, field: str, sample_array: list) -> (dict, list):
        """
        This method returns the frequency histogram of a specific field in:
        - a dictionary with the results in a structured visual form
        - a numpy array with the results

        :param sample_array: list : a subset from the array_values
        :param field: str: field to search for abnormal values
        :return: (dict: that contains the results in a structured form, list: contains the results in numpy form)
        """
        # initialize
        visual_results = {}
        temp_lis = []

        sub_array = [arr[field] for arr in sample_array]
        d_type = self.rate_specs[field][unit]
        # count frequency of each value
        counts = Counter(sub_array)
        # create results
        for k, v in counts.items():
            dic = create_structured_dict("frequency", field, v, k, d_type)
            temp_lis.append(dic)

        visual_results["frequency_histogram_of_{}".format(field)] = temp_lis

        return visual_results, sub_array

    def health_analyzer_first_solution(self, source_field: str, specific_value: float, target_field: str) -> (dict, list):
        """
        This method finds from a specific field a specific value, both given by the user, returns:
        - a dictionary with the results in a structured visual form
        - a numpy array with the results

        :param source_field: str: field to search
        :param target_field: str: field to show
        :param specific_value: float: specific value to search
        :return: (dict: that contains the results in a structured form, list: contains the results in numpy form)
        """
        # initialize
        visual_results = {}

        sub_array = [arr[source_field] for arr in self.array_values]
        # get matching values
        results_match = linear_search_equals(sub_array, specific_value)

        # select specific indices in a multi-D list
        arr_results = [ele for idx, ele in enumerate(self.array_values) if idx in results_match]
        # create virtual results
        visual_results["in_field_'{}'_value_'{}'_exists".format(source_field, specific_value)] = \
            len(arr_results)
        visual_results["details"] = arr_results
        # create results for plot
        arr_results_field = [ele[target_field] for ele in arr_results]

        return visual_results, arr_results_field

    def run(self, field: str, field_value: int or float, target_field: str,
            sample_size=0, print_results=True, path_to_save=""):
        """
        This method runs the analytics and is able to print the results as well as to design the histograms

        :param field: str: field to run the analytic
        :param field_value: int or float: value that is used from analytic health analyzer
        :param target_field: str: is used from analytic health analyzer
        :param sample_size: int: size of the sample in percentage related to self.array_values
        :param print_results: boolean: if true then will print the results and will design the histograms
        :param path_to_save: str: the absolute path to save the plots
        :return: None
        """

        if sample_size == 0:
            sample_size_int = int(len(self.array_values) * 0.1)
        else:
            sample_size_int = int(sample_size)

        sample_array = self.get_sample_array(sample_size_int)

        visual_results_abnormal_values, arr_abnormal_values = \
            self.find_abnormal_values(field, sample_array)

        visual_results_frequency_histogram, arr_frequency_histogram = \
            self.frequency_histogram_first_solution(field, sample_array)

        visual_results_health_analyzer, arr_health_analyzer = \
            self.health_analyzer_first_solution(field, field_value, target_field)

        if print_results:
            # print results
            print_data(visual_results_abnormal_values)
            print_data(visual_results_frequency_histogram)
            print_data(visual_results_health_analyzer)
            # print plot
            visualize_results_simple_plot(
                arr_abnormal_values[0], arr_abnormal_values[1], "abnormal_values",
                x_label="timestamp",
                y_label="pulse rate",
                line=False,
                path_to_save=path_to_save
            )
            # print histograms
            visualize_results_hist(
                arr_frequency_histogram, "frequency_histogram", x_label="frequency", y_label="values",
                path_to_save=path_to_save
            )
            visualize_results_hist(
                arr_health_analyzer, "health_analyzer for {} at value {}".format(field, field_value),
                x_label="frequency",
                y_label="heart_rate",
                path_to_save=path_to_save
            )


def run_first_solution(rate_specs, field, field_value, target_field, path_to_save, n=1000):
    # create measurements array
    array_measurements_first_solution = my_health_care_numpy(rate_specs, n)
    # initialize class
    analytics_first_solution = AnalyticsFirstSolution(array_measurements=array_measurements_first_solution, rate_specs=rate_specs)
    # produce results
    analytics_first_solution.run(
        field=field, field_value=field_value, target_field=target_field, path_to_save=path_to_save)


def benchmark_first_solution(rate_specs, field, field_value, target_field, path_to_save):
    n_samples = [1000, 2500, 5000, 7500, 10000, 12500, 15000]
    benchmark_array_n = []
    benchmark_array_time = []
    for idx, n in enumerate(n_samples):
        start_time = time.time()
        # generate records
        my_array_measurements_benchmark = my_health_care_numpy(rate_specs, n)
        # initialize class
        analytics_first_solution_benchmark = AnalyticsFirstSolution(
            array_measurements=my_array_measurements_benchmark, rate_specs=rate_specs)
        # produce results
        analytics_first_solution_benchmark.run(
            field=field, field_value=field_value, print_results=False, target_field=target_field)

        end_time = time.time() - start_time
        benchmark_array_n.append(n)
        benchmark_array_time.append(end_time * 1000)
        print("iteration of {} samples finished in {} milliseconds".format(n, end_time))

    # create benchmark plot
    visualize_results_simple_plot(
        x=benchmark_array_n,
        y=benchmark_array_time,
        title="benchmark results".format(n_samples),
        x_label="records",
        y_label="time in milliseconds",
        path_to_save=path_to_save
    )