import time
import numpy as np
import json

from main.user_defined_constants import unit, normal, max, min, range_values
from main.public_functions import create_structured_dict, print_data, \
    linear_search_equals, linear_search_bigger, linear_search_smaller, \
    visualize_results_simple_plot, visualize_results_hist


def my_health_care_numpy(rates_values_dict: dict, n: int) -> (np.array, dict):
    """
    This function generates the measurements array, based on n sample by using numpy arrays

    :param rates_values_dict: dict: dictionary that contains data specifications
    :param n: int: n amount of records
    :return: (np.array: array_measurements, dict: mapping of columns names)
    """
    # initialize
    my_array_mapping = {}
    rates_values_dict_copy = rates_values_dict.copy()
    del rates_values_dict_copy["timestamp"]
    my_array = np.empty((len(rates_values_dict_copy)+1, n))
    np.random.seed(109)
    # map column name with column position in numpy array
    my_array_mapping["timestamp"] = 0
    # create timestamp based on n
    my_array[0] = np.arange(start=0, stop=n, step=1, dtype=int)
    # generate measurements according the data specifications for n records
    for idx, (key, value) in enumerate(rates_values_dict_copy.items(), start=1):
        my_array_mapping[key] = idx
        if value[unit] == "int":
            my_array[idx] = np.random.randint(value[range_values][min], value[range_values][max] + 1, size=n)
        elif value[unit] == "float":
            my_array[idx] = np.random.randint(value[range_values][min] * 10, value[range_values][max] * 10 + 1, size=n) / 10

    return my_array.transpose(), my_array_mapping


class AnalyticsSecondSolution:
    """
    This class contains all the analytics
    """
    def __init__(self, array_measurements: np.array, array_mapping: dict, rate_specs: dict):
        """
        Initialize function of class

        :param array_measurements: np.arrray : numpy array containing the measurements
        :param array_mapping: dict: contains the names of the columns mapped with the column position within numpy.array
        :param rate_specs: dict: dictionary that contains data specifications
        """
        self.array_values = array_measurements
        self.array_mapping = array_mapping
        self.rate_specs = rate_specs

    def get_sample_array(self, sample_size: int) -> np.array:
        """
        This method gets a subset from the array_values

        :param sample_size: int : indicates the sample that will be used from the self array
        :return: np.array: a sample_array based on size
        """

        sample_indexes = np.random.choice(self.array_values.shape[0], sample_size)
        sample_array = self.array_values[sample_indexes, :]

        return sample_array

    def get_sub_array_column(self, field: str, array: np.array) -> (np.array, int):
        """
        This method gets a subset of the array given based on the field specified as well as the column's index
        :param field: str: field to contain
        :param array: np.array: array given
        :return: (np.array: an 1-D array, int: column_idx)
        """

        column = self.array_mapping[field]
        sub_array = array[:, column]

        return sub_array, column

    def find_abnormal_values_numpy(self, field: str, sample_array: np.array) -> (dict, np.array):
        """
        This method finds abnormal values on a specific field, given by the user, and returns:
        - a dictionary with the results in a structured visual form
        - a numpy array with the results

        :param sample_array: np.array : a subset from the array_values
        :param field: str: field to search for abnormal values
        :return: (dict: that contains the results in a structured form, np.array: contains the results in numpy form)
        """

        # initialize
        visual_results = {}
        temp_lis = []

        sub_array, column = self.get_sub_array_column(field, sample_array)
        d_type = self.rate_specs[field][unit]

        if d_type == "int":
            step = 1
        else:
            step = 0.1
        # get abnormal values from data specifications
        abnormal_values_min = self.rate_specs[field][normal][min] - step
        abnormal_values_max = self.rate_specs[field][normal][max] + step
        # find abnormal values
        res_match_min = list(np.where(sub_array <= abnormal_values_min)[0])
        res_match_max = list(np.where(sub_array >= abnormal_values_max)[0])
        res_match = res_match_min + res_match_max
        # select appropriate data from numpy array
        arr = sample_array[:, [0, column]]
        numpy_results = arr[res_match, :]

        # create results
        visual_results["abnormal_{}_count".format(field)] = len(res_match)

        for ele in numpy_results.tolist():
            dic = create_structured_dict("timestamp", field, ele[0], ele[1], d_type)
            temp_lis.append(dic)

        visual_results["abnormal_values"] = temp_lis

        return visual_results, numpy_results

    def frequency_histogram_numpy(self, field: str, sample_array: np.array) -> (dict, np.array):
        """
        This method returns the frequency histogram of a specific field in:
        - a dictionary with the results in a structured visual form
        - a numpy array with the results

        :param sample_array: np.array : a subset from the array_values
        :param field: str: field to search for abnormal values
        :return: (dict: that contains the results in a structured form, np.array: contains the results in numpy form)
        """
        # initialize
        visual_results = {}
        temp_lis = []

        sub_array, column = self.get_sub_array_column(field, sample_array)
        d_type = self.rate_specs[field][unit]
        # count frequency of each value
        unique, counts = np.unique(sub_array, return_counts=True)
        # create results
        for u, c in zip(counts, unique):
            dic = create_structured_dict("frequency", field, u, c, d_type)
            temp_lis.append(dic)

        visual_results["frequency_histogram_of_{}".format(field)] = temp_lis

        return visual_results, sub_array

    def health_analyzer_numpy(self, source_field: str, specific_value: float, target_field: str) -> (dict, np.array):
        """
        This method finds from a specific field a specific value, both given by the user, returns:
        - a dictionary with the results in a structured visual form
        - a numpy array with the results

        :param source_field: str: field to search
        :param target_field: str: field to show
        :param specific_value: float: specific value to search
        :return: (dict: that contains the results in a structured form, np.array: contains the results in numpy form)
        """
        # initialize
        visual_results = {}
        lis_dict = []
        temp_dict = {}

        sub_array, column_source = self.get_sub_array_column(source_field, self.array_values)
        column_target = self.array_mapping[target_field]
        res_dic = self.array_mapping.copy()
        # get matching values
        results_match = list(np.where(sub_array == specific_value)[0])

        # select specific indices in a multi-D np.array
        arr_results_numpy = self.array_values[results_match, :]
        # create structured dict to print
        for row in arr_results_numpy.tolist():
            for k, v in res_dic.items():
                temp_dict[k] = int(row[v]) if self.rate_specs[k][unit] == 'int' else float(row[v])
            lis_dict.append(temp_dict.copy())

        visual_results["in_field_'{}'_value_'{}'_exists".format(source_field, specific_value)] = \
            len(arr_results_numpy.tolist())
        visual_results["details"] = lis_dict

        arr_results_numpy = arr_results_numpy[:, column_target]

        return visual_results, arr_results_numpy

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

        visual_results_abnormal_values, numpy_arr_abnormal_values = \
            self.find_abnormal_values_numpy(field, sample_array)
        visual_results_frequency_histogram, numpy_arr_frequency_histogram = \
            self.frequency_histogram_numpy(field, sample_array)

        visual_results_health_analyzer, numpy_arr_health_analyzer = \
            self.health_analyzer_numpy(field, field_value, target_field)

        if print_results:
            # print results
            print_data(visual_results_abnormal_values)
            print_data(visual_results_frequency_histogram)
            print_data(visual_results_health_analyzer)
            # print histograms
            visualize_results_simple_plot(
                x=numpy_arr_abnormal_values[:, 0],
                y=numpy_arr_abnormal_values[:, 1],
                title="abnormal_values",
                x_label="timestamp",
                y_label="pulse rate",
                line=False,
                path_to_save=path_to_save
            )
            visualize_results_hist(
                arr_results=numpy_arr_frequency_histogram,
                title="frequency_histogram",
                x_label="pulse",
                y_label="frequency",
                path_to_save=path_to_save
            )
            visualize_results_hist(
                arr_results=numpy_arr_health_analyzer,
                title="health_analyzer for {} at value {}".format(field, field_value),
                x_label="heart_rate",
                y_label="frequency",
                path_to_save=path_to_save
            )


def run_second_solution(rate_specs, field, field_value, target_field, path_to_save, n=1000):
    # create measurements array
    my_array_measurements_second_solution, my_array_mapping_second_solution = my_health_care_numpy(rate_specs, n)
    # initialize class
    analytics_second_solution = AnalyticsSecondSolution(
        array_measurements=my_array_measurements_second_solution, array_mapping=my_array_mapping_second_solution,
        rate_specs=rate_specs)
    # produce results
    analytics_second_solution.run(
        field=field, field_value=field_value, target_field=target_field, path_to_save=path_to_save)


def benchmark_second_solution(rate_specs, field, field_value, target_field, path_to_save):
    # BENCHMARK
    n_samples = [1000, 2500, 5000, 7500, 10000, 12500, 15000]
    benchmark_list_second_solution = []

    for idx, n in enumerate(n_samples):
        start_time = time.time()
        # generate records
        my_array_measurements_benchmark_second_solution, my_array_mapping_benchmark_second_solution = \
            my_health_care_numpy(rate_specs, n)
        # initialize class
        analytics_second_solution_benchmark = AnalyticsSecondSolution(
            array_measurements=my_array_measurements_benchmark_second_solution,
            array_mapping=my_array_mapping_benchmark_second_solution,
            rate_specs=rate_specs)
        # produce results
        analytics_second_solution_benchmark.run(
            field=field, field_value=field_value, print_results=False, target_field=target_field)
        end_time = time.time() - start_time
        benchmark_list_second_solution.append([n, end_time * 1000])
        print("iteration of {} samples finished in {} milliseconds".format(n, end_time))

    # create benchmark plot
    benchmark_numpy_array = np.array(benchmark_list_second_solution)
    visualize_results_simple_plot(
        x=benchmark_numpy_array[:, 0],
        y=benchmark_numpy_array[:, 1],
        title="benchmark results".format(n_samples),
        x_label="records",
        y_label="time in milliseconds",
        path_to_save=path_to_save
    )