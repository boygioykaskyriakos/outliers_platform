import pandas as pd

from copy import copy

from outlier_algorithms.base_class_outlier_algorithms import BaseClassOutlierAlgorithms
from static_files.standard_variable_names import VALUES, VALUE, KEY, OUTLIER_NO, \
    HIGHER_RANGE_NUMBER, LOWER_RANGE_NUMBER, EXCEPTION
from static_files.dixon_formulas import r0, r10, r11, r21, r22, generic_formula_dixon_q_test


class FindOutlierDixon(BaseClassOutlierAlgorithms):
    def __init__(self, grouped_data: pd.DataFrame):
        super().__init__()

        self.grouped_data = grouped_data
        self.static_n = self.read_ini_file_obj.get_int("DIXON_Q_TEST_SUBSET_VARIABLES", "static_n")
        self.static_n_maximum = self.read_ini_file_obj.get_int("DIXON_Q_TEST_SUBSET_VARIABLES", "static_n_maximum")
        self.critical_value = self.read_ini_file_obj.get_int("DIXON_Q_TEST_SUBSET_VARIABLES", "critical_value")

    @staticmethod
    def dixon_q_test_algo(numbers: pd.Series, comparator: float) -> bool:
        """
        Dixon q test method reflects the exact dixon q test algorithm

        :param numbers: list : the subset to examine if it contains outliers
        :param comparator: float: the value to compare for outliers according the dixon-q-test algorithm
        :return: bool: True or False
        """

        # initialize local variables
        numbers = copy(numbers).sort_values().to_list()
        len_numbers = len(numbers)

        q_lower = 0
        q_upper = 0

        if len_numbers < r0[HIGHER_RANGE_NUMBER]:
            raise ValueError(r0[EXCEPTION])
        # r10
        elif r10[LOWER_RANGE_NUMBER] <= len_numbers <= r10[HIGHER_RANGE_NUMBER]:
            r = r10
        # r11
        elif r11[LOWER_RANGE_NUMBER] <= len_numbers <= r11[HIGHER_RANGE_NUMBER]:
            r = r11
        # r21
        elif r21[LOWER_RANGE_NUMBER] <= len_numbers <= r21[HIGHER_RANGE_NUMBER]:
            r = r21
        else:   # r22[LOWER_RANGE_NUMBER] <= len_numbers
            r = r22

        upper_numerator, upper_denominator, lower_numerator, lower_denominator = \
            generic_formula_dixon_q_test(r, numbers)

        # apply dixon q test algorithm logic
        if lower_denominator > 0:
            q_lower = lower_numerator / lower_denominator

        if upper_denominator > 0:
            q_upper = upper_numerator / upper_denominator

        if q_lower > comparator or q_upper > comparator:
            return True
        else:
            return False

    @staticmethod
    def find_comparator(numbers: list, confidence: tuple) -> float:
        get_number = len(numbers) - 3

        return confidence[get_number]

    def get_results_per_subset(
            self, static_n: int, grp: pd.DataFrame, confidence: dict, result: list) -> list:

        test_set = grp[VALUES]

        # list comprehension with UDF optimized on pd.DataFrame
        # read it like: for i in range if condition is true then print
        result += [
            self.results_to_dict(static_n, grp, test_set[i+static_n:i + 2*static_n].sort_values(), i)
            for i in range(len(test_set)-2*static_n + 1)
            if self.dixon_q_test_algo(
                test_set[i+static_n:i + 2*static_n],
                self.find_comparator(test_set[i+static_n:i+2*static_n], confidence[VALUE])
            ) is True
        ]

        return result

    def run(self, confidence_level: dict) -> None:
        """
        The main method of the class that saves to file the outliers according the dixon-q-test algorithm

        :param confidence_level: dict: as key contains the title of the confidence
        and as values contains the dixon-q-test comparator values
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
                lambda grp: self.get_results_per_subset(static_n, grp, confidence_level, final_result)
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

