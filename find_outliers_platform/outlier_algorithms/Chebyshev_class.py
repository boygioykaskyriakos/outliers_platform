import pandas as pd
import statistics
import math

from copy import copy

from outlier_algorithms.base_class_outlier_algorithms import BaseClassOutlierAlgorithms
from static_files.standard_variable_names import VALUES, OUTLIER_NO, SUBSET_SIZE, SUBSET, MAX_VALUE, MIN_VALUE, \
    ACCEPTABLE_DEVIATION, VALUE_TO_CHECK, OUTLIER_SCORE


class FindOutlierChebyshev(BaseClassOutlierAlgorithms):
    def __init__(self, grouped_data: pd.DataFrame):
        super().__init__()

        self.grouped_data = grouped_data
        self.static_n = self.read_ini_file_obj.get_int("CHEBYSHEV_SUBSET_VARIABLES", "static_n")
        self.static_n_maximum = self.read_ini_file_obj.get_int("CHEBYSHEV_SUBSET_VARIABLES", "static_n_maximum")
        self.critical_value = self.read_ini_file_obj.get_int("CHEBYSHEV_SUBSET_VARIABLES", "critical_value")
        self.probability_threshold = \
            self.read_ini_file_obj.get_float("CHEBYSHEV_SUBSET_VARIABLES", "probability_threshold")
        self.chebyshev_k = self.get_k()
        self.OUTPUT_COLUMNS_DETAILS_GENERAL += [OUTLIER_SCORE, ACCEPTABLE_DEVIATION, VALUE_TO_CHECK, MIN_VALUE, MAX_VALUE]

    def get_k(self):
        if abs(self.probability_threshold) > 1:
            return 0

        k = math.sqrt(1. / (1. - self.probability_threshold))
        return k

    def chebushev_algo(self, subset: pd.Series) -> bool:
        outlier_score = 0
        subset_statistics = subset.to_list()[:-1]
        value_to_check = subset.to_list()[-1]
        # get mean and standard deviation
        sample_mean = statistics.mean(subset_statistics)
        sample_std_dev = statistics.stdev(subset_statistics)

        acceptable_deviation = self.chebyshev_k * sample_std_dev

        if sample_std_dev > 1 and acceptable_deviation != 0:
            outlier_score = abs(value_to_check - sample_mean) / acceptable_deviation

        if outlier_score > 1:
            return True
        else:
            return False

    def get_results_per_subset(
            self, static_n: int, grp: pd.DataFrame, result: list) -> list:

        test_set = grp[VALUES]

        # list comprehension with UDF optimized on pd.DataFrame
        # read it like: for i in range if condition is true then...
        result += [
            self.results_to_dict(static_n, grp, test_set[i+static_n:i + 2*static_n], i, chebyshev_k=self.chebyshev_k)
            for i in range(len(test_set)-2*static_n + 1)
            if self.chebushev_algo(test_set[i+static_n:i + 2*static_n]) is True
        ]

        return result

    def run(self) -> None:
        """
        The main method of the class that saves to file the outliers according the Chebyshev algorithm
        :return: None
        """

        # initialize local variables
        static_n = copy(self.static_n)
        final_result = []
        df_metrics_details_general = pd.DataFrame(columns=self.OUTPUT_COLUMNS_DETAILS_GENERAL)
        df_metrics_summary = pd.DataFrame(columns=self.OUTPUT_COLUMNS_SUMMARY)
        df_metrics_details_critical = pd.DataFrame(columns=self.OUTPUT_COLUMNS_DETAILS_CRITICAL)

        # apply logic main loop
        while static_n <= self.static_n_maximum:
            self.grouped_data.apply(
                lambda grp: self.get_results_per_subset(static_n, grp, final_result)
            )
            static_n += 1

        # create results
        if len(final_result) > 0:
            for idx, row in enumerate(final_result):
                row[OUTLIER_NO] = idx+1

            if self.print_debug:
                for row in final_result:
                    self.print_to_console(row)

            df_metrics_details_general = pd.DataFrame(final_result)
            df_metrics_details_critical = self.format_metrics_critical(df_metrics_details_general, self.critical_value)
            df_metrics_summary = self.format_metrics_summary(df_metrics_details_general, df_metrics_details_critical)

        # save results to files
        self.save_file.run(df_metrics_details_general[self.OUTPUT_COLUMNS_DETAILS_GENERAL], "metrics_details_generic")
        self.save_file.run(
            df_metrics_details_critical[self.OUTPUT_COLUMNS_DETAILS_CRITICAL], "metrics_details_critical")
        self.save_file.run(df_metrics_summary[self.OUTPUT_COLUMNS_SUMMARY], "metrics_summary")
