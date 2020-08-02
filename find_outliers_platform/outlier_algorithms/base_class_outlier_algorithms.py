import pandas as pd


from base_class.base_class_analytic import BaseClassAnalytic
from static_files.standard_variable_names import DATA_TYPE, NODE, VALUES, VALUE, KEY, \
    OUTLIER_NO, SUBSET, SUBSET_SIZE, INDEX_FIRST_ELEMENT, INDEX_LAST_ELEMENT, TOTAL_PANICS, \
    HIGHER_RANGE_NUMBER, LOWER_RANGE_NUMBER, EXCEPTION


class BaseClassOutlierAlgorithms(BaseClassAnalytic):
    OUTPUT_COLUMNS = [OUTLIER_NO, SUBSET_SIZE, SUBSET, NODE, DATA_TYPE, INDEX_FIRST_ELEMENT, INDEX_LAST_ELEMENT]
    OUTPUT_COLUMNS_METRICS = [SUBSET_SIZE, OUTLIER_NO]
    OUTPUT_COLUMNS_METRICS_CRITICAL = [SUBSET_SIZE, TOTAL_PANICS]

    def __init__(self):
        """
        for now empty
        """
        pass

    @staticmethod
    def results_to_dict(
            static_n: int, whole_set: pd.DataFrame, temp_data: pd.Series, i: int) -> dict:
        temp_dic_res = {
            SUBSET_SIZE: str(static_n),
            SUBSET: str(temp_data.tolist()),
            NODE: str(whole_set[NODE].values[0]).replace("\t", ""),
            DATA_TYPE: whole_set[DATA_TYPE].values[0],
            INDEX_FIRST_ELEMENT: str(i + static_n),
            INDEX_LAST_ELEMENT: str(i + 2 * static_n - 1),

        }

        return temp_dic_res

    def print_to_console(self, row: dict, confidence_lvl=None) -> None:
        msg = "********** OUTLIER No " + str(row[OUTLIER_NO]) + " *******************" + "\n"
        msg += "NODE: " + row[NODE] + ", DATA TYPE [" + row[DATA_TYPE] + "]\n"
        msg += "INDEX[" + row[INDEX_FIRST_ELEMENT] + ", " + row[INDEX_LAST_ELEMENT] + "] = "
        msg += row[SUBSET] + " " + "\n"
        if confidence_lvl:
            msg += confidence_lvl[KEY].upper() + ", SUBSET SIZE: " + row[SUBSET_SIZE] + "\n"

        self.logger.info(msg)

    @staticmethod
    def format_metrics_critical(df: pd.DataFrame, critical_value: float) -> pd.DataFrame:
        df = df.groupby(
            [SUBSET_SIZE, NODE, INDEX_FIRST_ELEMENT, INDEX_LAST_ELEMENT]
        ).count().reset_index()

        df = df[df[OUTLIER_NO] > critical_value]
        df = df.groupby(SUBSET_SIZE)[OUTLIER_NO].sum().reset_index()
        df[OUTLIER_NO] = df[OUTLIER_NO] / 2
        df[OUTLIER_NO] = df[OUTLIER_NO].astype(int)
        df = df.rename(columns={OUTLIER_NO: TOTAL_PANICS})

        return df

    def run(self, *args):
        raise NotImplementedError("method not implemented")
