import pandas as pd
import statistics
import math

from copy import copy

from outlier_algorithms.base_class_outlier_algorithms import BaseClassOutlierAlgorithms
from static_files.standard_variable_names import VALUES, OUTLIER_NO, SUBSET_SIZE, MAX_VALUE, MIN_VALUE, \
    ACCEPTABLE_DEVIATION, VALUE_TO_CHECK, OUTLIER_SCORE, NODE, VALUE, KEY


class FindOutlierChebyshevInequality(BaseClassOutlierAlgorithms):
    """
    This Class implements the Chebyshev Inequality outlier method
    """
    def __init__(self, grouped_data: pd.DataFrame):
        super().__init__()

        self.grouped_data = grouped_data
        self.static_n = self.read_ini_file_obj.get_int("CHEBYSHEV_SUBSET_VARIABLES", "static_n")
        self.static_n_maximum = self.read_ini_file_obj.get_int("CHEBYSHEV_SUBSET_VARIABLES", "static_n_maximum")
        self.critical_value = self.read_ini_file_obj.get_int("CHEBYSHEV_SUBSET_VARIABLES", "critical_value")
        self.OUTPUT_COLUMNS_DETAILS_GENERAL += [OUTLIER_SCORE, ACCEPTABLE_DEVIATION, VALUE_TO_CHECK, MIN_VALUE, MAX_VALUE]

    @staticmethod
    def get_chebyshev_k(probability_threshold: float):
        """
        This method calculates the chebyshev K constant based on the probability threshold

        :param probability_threshold: float: the probability threshold
        :return: float: the chebyshev K
        """
        if abs(probability_threshold) > 1:
            return 0

        k = math.sqrt(1. / (1. - probability_threshold))
        return k

    @staticmethod
    def chebushev_inequality_algorithm(subset: pd.Series, chebyshev_k: float) -> bool:
        """
        This method implements the chebysevn inequality algorithm
        and determines if the current sequence contains an outlier

        :param subset: pd.Series: a subset of numbers
        :param chebyshev_k: float: the Chebyshev K constant based on probability threshold
        :return: bool: true if outlier exists false if not
        """

        outlier_score = 0
        subset_statistics = subset.to_list()[:-1]
        value_to_check = subset.to_list()[-1]
        # get mean and standard deviation
        sample_mean = statistics.mean(subset_statistics)
        sample_std_dev = statistics.stdev(subset_statistics)

        acceptable_deviation = chebyshev_k * sample_std_dev

        if sample_std_dev > 1 and acceptable_deviation != 0:
            outlier_score = abs(value_to_check - sample_mean) / acceptable_deviation

        if outlier_score > 1:
            return True
        else:
            return False

    def results_to_dict(self, static_n: int, grp: pd.DataFrame, temp_data: pd.Series, i: int, chebyshev_k: float):
        """
        Extend method results to dict, by adding the chebyshev K variable as well

        :param static_n: int: number of elements
        :param grp: pd.DataFrame: the whole set of all the data for the specific group
        :param temp_data: pd.Series: the temporary data of the group
        :param i: int: the starting row of the first element of the set
        :param chebyshev_k: float: the Chebyshev K constant based on probability threshold
        :return: dict: the new dictionary of results
        """
        temp_dic = super(FindOutlierChebyshevInequality, self).results_to_dict(static_n, grp, temp_data, i)

        temp_data = temp_data.tolist()
        subset_statistics = temp_data[:-1]
        value_to_check = temp_data[-1]
        # get mean and standard deviation
        sample_mean = statistics.mean(subset_statistics)
        sample_std_dev = statistics.stdev(subset_statistics)
        acceptable_deviation = chebyshev_k * sample_std_dev
        outlier_score = abs(value_to_check - sample_mean) / acceptable_deviation
        min_value = sample_mean - acceptable_deviation
        max_value = sample_mean + acceptable_deviation

        temp_dic[OUTLIER_SCORE] = outlier_score
        temp_dic[ACCEPTABLE_DEVIATION] = acceptable_deviation
        temp_dic[VALUE_TO_CHECK] = value_to_check
        temp_dic[MIN_VALUE] = min_value
        temp_dic[MAX_VALUE] = max_value

        return temp_dic

    def get_results_per_subset(
            self, static_n: int, grp: pd.DataFrame, result: list, chebyshev_k: float) -> list:
        """
        This method returns the results for the specific static_n of elements for the specific group

        :param static_n: int: number of elements
        :param grp: pd.DataFrame: the whole set of all the data for the specific group
        :param result: list: a list of all the results of other subsets
        :param chebyshev_k: float: the Chebyshev K constant based on probability threshold
        :return: list: a list of results
        """

        test_set = grp[VALUES]

        # list comprehension with UDF optimized on pd.DataFrame
        # read it like: for i in range if condition is true then...
        result += [
            self.results_to_dict(static_n, grp, test_set[i + static_n:i + 2 * static_n], i, chebyshev_k)
            for i in range(len(test_set) - 2 * static_n + 1)
            if self.chebushev_inequality_algorithm(test_set[i + static_n:i + 2 * static_n], chebyshev_k) is True
        ]

        return result

    def run(self, confidence_level: dict) -> None:
        """
        The main method of the class that:
            - implements the Chebyshev Inequality algorithm
            - saves the results to file

        :return: None
        """

        # initialize local variables
        chebyshev_k = self.get_chebyshev_k(confidence_level[VALUE])
        static_n = copy(self.static_n)
        final_result = []
        df_metrics_details_general = pd.DataFrame(columns=self.OUTPUT_COLUMNS_DETAILS_GENERAL)
        df_metrics_summary = pd.DataFrame(columns=self.OUTPUT_COLUMNS_SUMMARY)
        df_metrics_details_critical = pd.DataFrame(columns=self.OUTPUT_COLUMNS_DETAILS_CRITICAL)

        # apply logic main loop
        while static_n <= self.static_n_maximum:
            self.grouped_data.apply(
                lambda grp: self.get_results_per_subset(static_n, grp, final_result, chebyshev_k)
            )
            static_n += 1

        # create results
        if len(final_result) > 0:
            for idx, row in enumerate(final_result):
                row[OUTLIER_NO] = idx+1

            if self.print_debug:
                for row in final_result:
                    self.print_to_console(row, confidence_level)

            df_metrics_details_general, df_metrics_details_critical, df_metrics_summary = \
                self.create_result_dfs(
                    final_result, self.critical_value,
                    df_metrics_details_general, df_metrics_details_critical, df_metrics_summary
                )

        # save results to files
        self.save_file.run(
            df_metrics_details_general[self.OUTPUT_COLUMNS_DETAILS_GENERAL],
            confidence_level[KEY] + "_metrics_details_generic"
        )
        self.save_file.run(
            df_metrics_details_critical[self.OUTPUT_COLUMNS_DETAILS_CRITICAL],
            confidence_level[KEY] + "_metrics_details_critical"
        )
        self.save_file.run(
            df_metrics_summary[self.OUTPUT_COLUMNS_SUMMARY], confidence_level[KEY] + "_metrics_summary"
        )
