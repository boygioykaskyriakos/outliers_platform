import pandas as pd
import statistics


from base_class.base_class_analytic import BaseClassAnalytic
from static_files.standard_variable_names import DATA_TYPE, NODE, KEY, \
    OUTLIER_NO, SUBSET, SUBSET_SIZE, INDEX_FIRST_ELEMENT, INDEX_LAST_ELEMENT, TOTAL_PANICS


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

        df[SUBSET_SIZE] = df[SUBSET_SIZE].astype(int)
        try:
            df[NODE] = df[NODE].astype(int)
        except ValueError:
            pass
        df = df.sort_values([SUBSET_SIZE, NODE])

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
        df_metrics_summary[SUBSET_SIZE] = df_metrics_summary[SUBSET_SIZE].astype(int)
        df_metrics_summary = df_metrics_summary.sort_values([SUBSET_SIZE])

        return df_metrics_summary

    @staticmethod
    def results_to_dict(static_n: int, whole_set: pd.DataFrame, temp_data: pd.Series, i: int) -> dict:
        temp_data = temp_data.tolist()
        temp_dic_res = {
            SUBSET_SIZE: str(static_n),
            SUBSET: str(temp_data),
            NODE: str(whole_set[NODE].values[0]).replace("\t", ""),
            DATA_TYPE: whole_set[DATA_TYPE].values[0],
            INDEX_FIRST_ELEMENT: str(i + static_n),
            INDEX_LAST_ELEMENT: str(i + 2 * static_n - 1),

        }

        return temp_dic_res

    def create_result_dfs(self, final_result: dict, critical_value: int) -> tuple:
        df_metrics_details_general = pd.DataFrame(final_result)
        df_metrics_details_general[SUBSET_SIZE] = df_metrics_details_general[SUBSET_SIZE].astype(int)

        try:
            df_metrics_details_general[NODE] = df_metrics_details_general[NODE].astype(int)
        except ValueError:
            pass

        df_metrics_details_general = df_metrics_details_general.sort_values([SUBSET_SIZE, NODE])

        df_metrics_details_critical = self.format_metrics_critical(df_metrics_details_general, critical_value)
        df_metrics_summary = self.format_metrics_summary(df_metrics_details_general, df_metrics_details_critical)

        return df_metrics_details_general, df_metrics_details_critical, df_metrics_summary

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
