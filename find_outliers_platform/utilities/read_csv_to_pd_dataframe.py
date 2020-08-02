import pandas as pd
import re

from base_class.base_class_analytic import BaseClassAnalytic
from static_files.standard_variable_names import NODE, TIME, DATA_TYPE, VALUES, RECEIVE_DATA_TAG, SEND_DATA_TAG, \
    RECEIVE_DATA_VALUE, SEND_DATA_VALUE


class ReadCSVToDataFrame(BaseClassAnalytic):
    def __init__(self, field_name: str, file_path: str, delimiter=""):
        BaseClassAnalytic.__init__(self)

        self.file_path = self.read_ini_file_obj.get_str(field_name, file_path)
        try:
            self.delimiter = self.read_ini_file_obj.get_str(field_name, delimiter)
        except Exception as e:
            print(e)
            self.delimiter = ""

    def normal_csv(self):
        if len(self.delimiter) > 0:
            df = pd.read_csv(self.file_path, delimiter=self.delimiter)
        else:
            df = pd.read_csv(self.file_path)

        return df

    def read_data_columns_to_rows(self) -> pd.DataFrame:
        with open(self.file_path, 'r') as in_file:
            data = []
            headers = in_file.readline().split()
            headers = [header.upper() for header in headers]
            next(in_file)
            for line in in_file:
                row_data = re.sub('\s+', ' ', line).split()
                data.append(row_data)

            df = pd.DataFrame(columns=headers, data=data)
            df = df.dropna()

        df_send = df[[NODE, TIME, SEND_DATA_TAG]]
        df_send = df_send.rename(columns={SEND_DATA_TAG: VALUES})
        df_send[DATA_TYPE] = SEND_DATA_VALUE

        df_receive = df[[NODE, TIME, RECEIVE_DATA_TAG]]
        df_receive = df_receive.rename(columns={RECEIVE_DATA_TAG: VALUES})
        df_receive[DATA_TYPE] = RECEIVE_DATA_VALUE

        df = pd.concat([df_send, df_receive])
        df[VALUES] = df[VALUES].astype(float)

        return df

    def run(self, normal=True) -> pd.DataFrame:
        if normal:
            return self.normal_csv()
        else:
            return self.read_data_columns_to_rows()
