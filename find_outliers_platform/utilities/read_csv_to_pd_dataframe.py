import pandas as pd
import re

from base_class.base_class_analytic import BaseClassAnalytic
from static_files.standard_variable_names import NODE, TIME, DATA_TYPE, VALUES, RECEIVE_DATA_TAG, SEND_DATA_TAG, \
    RECEIVE_DATA_VALUE, SEND_DATA_VALUE, INDEX_ORDER


class ReadCSVToDataFrame(BaseClassAnalytic):
    """
    This Child Class reads a csv from a path and converts it to a pandas DataFrame object
    """
    NORMAL_HEADERS = [NODE, TIME, DATA_TYPE, VALUES]

    def __init__(self, field_name: str, file_path: str, delimiter=""):
        """
        Initialize instance variables

        :param field_name: str: the ini title
        :param file_path: str: the ini field name
        :param delimiter: the delimiter of the csv file
        """
        BaseClassAnalytic.__init__(self)

        self.file_path = self.read_ini_file_obj.get_str(field_name, file_path)
        try:
            self.delimiter = self.read_ini_file_obj.get_str(field_name, delimiter)
        except Exception as e:
            print(e)
            self.delimiter = ""

    def normal_csv(self):
        """
        This method determines the delimiter

        :return: pd.DataFrame: returns the csv in pd.Dataframe form
        """
        if len(self.delimiter) > 0:
            df = pd.read_csv(self.file_path, delimiter=self.delimiter)
        else:
            df = pd.read_csv(self.file_path)

        return df

    def read_data_columns_to_rows(self) -> pd.DataFrame:
        """
        This method reads the csv file with the build in open method
        :return: pd.DataFrame: return the csv as pd.DataFrame object
        """
        with open(self.file_path, 'r') as in_file:
            data = []
            headers = in_file.readline().split()
            headers = [header.upper() for header in headers]
            next(in_file)
            for line in in_file:
                row_data = re.sub('\s+', ' ', line).split()
                data.append(row_data)

            df = pd.DataFrame(columns=headers, data=data)
            df[INDEX_ORDER] = df.index
            df = df.dropna()

        df_send = df[[INDEX_ORDER, NODE, TIME, SEND_DATA_TAG]]
        df_send = df_send.rename(columns={SEND_DATA_TAG: VALUES})
        df_send[DATA_TYPE] = SEND_DATA_VALUE
        df_send[INDEX_ORDER] = df_send[INDEX_ORDER]*2

        df_receive = df[[INDEX_ORDER, NODE, TIME, RECEIVE_DATA_TAG]]
        df_receive = df_receive.rename(columns={RECEIVE_DATA_TAG: VALUES})
        df_receive[DATA_TYPE] = RECEIVE_DATA_VALUE
        df_receive[INDEX_ORDER] = df_receive[INDEX_ORDER]*2+1

        df = pd.concat([df_send, df_receive])
        df[VALUES] = df[VALUES].astype(float)
        df = df.sort_values([INDEX_ORDER])
        df = df.drop([INDEX_ORDER], axis=1)
        df = df.reset_index()

        df = df[[NODE, TIME, DATA_TYPE, VALUES]]

        return df

    def run(self) -> pd.DataFrame:
        """
        The main method of the class, reads the csv and returns a pandas DataFrame object.
        :return: pd.DataFrame: csv to pd.DataFrame object
        """
        with open(self.file_path, 'r') as in_file:
            headers = in_file.readline()
            headers = headers.replace("\n", "")

            if ',' in headers:
                headers = headers.split(',')
            else:
                headers = headers.split()

        if headers == self.NORMAL_HEADERS:
            return self.normal_csv()
        else:
            return self.read_data_columns_to_rows()
