import pandas as pd
import statistics


from base_class.base_class_analytic import BaseClassAnalytic
from static_files.standard_variable_names import DATA_TYPE, NODE, KEY, \
    OUTLIER_NO, SUBSET, SUBSET_SIZE, INDEX_FIRST_ELEMENT, INDEX_LAST_ELEMENT, TOTAL_PANICS, \
    MAX_VALUE, MIN_VALUE, ACCEPTABLE_DEVIATION, VALUE_TO_CHECK, OUTLIER_SCORE


class BaseClassOutlierAlgorithms(BaseClassAnalytic):
    OUTPUT_COLUMNS_DETAILS_GENERAL = \
        [OUTLIER_NO, SUBSET_SIZE, SUBSET, NODE, DATA_TYPE, INDEX_FIRST_ELEMENT, INDEX_LAST_ELEMENT]
    OUTPUT_COLUMNS_DETAILS_CRITICAL = [
        SUBSET_SIZE, NODE, DATA_TYPE, INDEX_FIRST_ELEMENT, INDEX_LAST_ELEMENT, TOTAL_PANICS, SUBSET
    ]
    OUTPUT_COLUMNS_SUMMARY = [SUBSET_SIZE, OUTLIER_NO, TOTAL_PANICS]

    @staticmethod
    def format_metrics_critical(df_all_data: pd.DataFrame, critical_value: float) -> pd.DataFrame:
        df = df_all_data.groupby(
            [SUBSET_SIZE, NODE, INDEX_FIRST_ELEMENT, INDEX_LAST_ELEMENT]
        ).count().reset_index()

        df = pd.merge(
            df[[SUBSET_SIZE, NODE, INDEX_FIRST_ELEMENT, INDEX_LAST_ELEMENT, OUTLIER_NO]],
            df_all_data[[SUBSET_SIZE, NODE, DATA_TYPE, INDEX_FIRST_ELEMENT, INDEX_LAST_ELEMENT, SUBSET]],
            on=[SUBSET_SIZE, NODE, INDEX_FIRST_ELEMENT, INDEX_LAST_ELEMENT],
            how='left'
        )

        df = df[df[OUTLIER_NO] > critical_value]
        df_per_node = df.groupby([SUBSET_SIZE, NODE])[OUTLIER_NO].sum().reset_index()

        df = pd.merge(
            df[[SUBSET_SIZE, NODE, DATA_TYPE, INDEX_FIRST_ELEMENT, INDEX_LAST_ELEMENT, SUBSET]],
            df_per_node,
            on=[SUBSET_SIZE, NODE],
            how='left'
        )

        df[OUTLIER_NO] = df[OUTLIER_NO] / 4
        df[OUTLIER_NO] = df[OUTLIER_NO].astype(int)
        df = df.rename(columns={OUTLIER_NO: TOTAL_PANICS})

        return df

    @staticmethod
    def format_metrics_summary(df_metrics_general: pd.DataFrame, df_metrics_critical: pd.DataFrame) -> pd.DataFrame:
        df_metrics_summary = df_metrics_general.groupby([SUBSET_SIZE]).count().reset_index()

        df_metrics_critical = df_metrics_critical[[SUBSET_SIZE, NODE, TOTAL_PANICS]].drop_duplicates().reset_index()
        df_metrics_critical = df_metrics_critical.groupby([SUBSET_SIZE]).count().reset_index()

        df_metrics_summary = pd.merge(
            df_metrics_summary[[SUBSET_SIZE, OUTLIER_NO]],
            df_metrics_critical[[SUBSET_SIZE, TOTAL_PANICS]],
            on=[SUBSET_SIZE],
            how='left'
        )

        return df_metrics_summary

    def results_to_dict(
            self,
            static_n: int, whole_set: pd.DataFrame, temp_data: pd.Series, i: int, chebyshev_k=None) -> dict:

        temp_data = temp_data.tolist()
        temp_dic_res = {
            SUBSET_SIZE: str(static_n),
            SUBSET: str(temp_data),
            NODE: str(whole_set[NODE].values[0]).replace("\t", ""),
            DATA_TYPE: whole_set[DATA_TYPE].values[0],
            INDEX_FIRST_ELEMENT: str(i + static_n),
            INDEX_LAST_ELEMENT: str(i + 2 * static_n - 1),

        }
        if chebyshev_k is not None:
            temp_dic_res = self.get_detailed_statistics_chebyshev(temp_dic_res, temp_data, chebyshev_k)

        return temp_dic_res

    @staticmethod
    def get_detailed_statistics_chebyshev(temp_dic, temp_data, chebyshev_k):
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

    def print_to_console(self, row: dict, confidence_lvl=None) -> None:
        msg = "********** OUTLIER No " + str(row[OUTLIER_NO]) + " *******************" + "\n"
        msg += "NODE: " + row[NODE] + ", DATA TYPE [" + row[DATA_TYPE] + "]\n"
        msg += "INDEX[" + row[INDEX_FIRST_ELEMENT] + ", " + row[INDEX_LAST_ELEMENT] + "] = "
        msg += row[SUBSET] + " " + "\n"
        if confidence_lvl:
            msg += confidence_lvl[KEY].upper() + ", SUBSET SIZE: " + row[SUBSET_SIZE] + "\n"

        self.logger.info(msg)

    def run(self, *args):
        raise NotImplementedError("method not implemented")
