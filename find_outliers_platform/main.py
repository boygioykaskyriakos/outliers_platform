from static_files.confidence_data import CONFIDENCE_DIXON_Q_TEST_STATIC_Q95, CONFIDENCE_DIXON_Q_TEST_STATIC_Q90, \
    CONFIDENCE_DIXON_Q_TEST_STATIC_Q99, CONFIDENCE_CHEBYSHEV_STATIC_Q90, CONFIDENCE_CHEBYSHEV_STATIC_Q95, \
    CONFIDENCE_CHEBYSHEV_STATIC_Q99
from utilities.read_csv_to_pd_dataframe import ReadCSVToDataFrame
from utilities.read_ini_file import ReadIniFile
from static_files.standard_variable_names import NODE, DATA_TYPE
from outlier_algorithms.dixon_q_test_class import FindOutlierDixon
from outlier_algorithms.chebyshev_class import FindOutlierChebyshevInequality

if __name__ == "__main__":
    read_ini_obj = ReadIniFile()
    # results for dixon_q_test
    find_outliers_dixon_switch = read_ini_obj.get_boolean("ALGORITHMS_TO_RUN", "dixon_q_test")
    if find_outliers_dixon_switch:
        df_data = ReadCSVToDataFrame(field_name="DATA_SET_INFO", file_path="full_file_path", delimiter="delimiter").run()
        df_data_grouped = df_data.groupby([NODE, DATA_TYPE])

        # results for Dixon
        find_outliers_dixon = FindOutlierDixon(grouped_data=df_data_grouped)

        # results for q90
        find_outliers_dixon.run(CONFIDENCE_DIXON_Q_TEST_STATIC_Q90)

        # results for q95
        find_outliers_dixon.run(CONFIDENCE_DIXON_Q_TEST_STATIC_Q95)

        # results for q99
        find_outliers_dixon.run(CONFIDENCE_DIXON_Q_TEST_STATIC_Q99)

    # results for Chebyshev
    find_outliers_chebyshev_switch = read_ini_obj.get_boolean("ALGORITHMS_TO_RUN", "chebyshev")
    if find_outliers_chebyshev_switch:
        df_data = ReadCSVToDataFrame(
            field_name="DATA_SET_INFO_SECOND_TYPE", file_path="full_file_path", delimiter="delimiter").run()
        df_data_grouped = df_data.groupby([NODE, DATA_TYPE])

        find_outliers_chebyshev = FindOutlierChebyshevInequality(grouped_data=df_data_grouped)

        find_outliers_chebyshev.run(CONFIDENCE_CHEBYSHEV_STATIC_Q90)

        find_outliers_chebyshev.run(CONFIDENCE_CHEBYSHEV_STATIC_Q95)

        find_outliers_chebyshev.run(CONFIDENCE_CHEBYSHEV_STATIC_Q99)


