import pandas as pd
import inspect

from utilities.log_module import Logger


class SavePdToCSVFile:
    """
    This class saves a pandas data frame to csv file
    """
    def __init__(self, output_path: str):
        """
        Initialization of instance variable
        :param output_path: The output path that the file will be saved
        """
        self.output_path = output_path
        self.logger = Logger()

    def run(self, df: pd.DataFrame, title=""):
        """
        This method gets a data frame and a string title and saves the data frame to csv,
        The csv file name consists:
            - of the class that is calling this method,
            - is also appending the title variable to the file name

        :param df: the data frame to be saved
        :param title: the title to be added to the file name
        :return: None
        """
        class_function_name = []
        stack = inspect.stack()

        # get the child class' name that is calling this method
        for row in stack:
            if "self" in row[0].f_locals.keys():
                if row[0].f_locals["self"].__class__.__name__ == self.__class__.__name__:
                    continue
                else:
                    class_function_name = row[0].f_locals["self"].__class__.__name__ + "_"
                    break

        if title != "":
            title = "_".join([title])

        full_output_path = "\\".join([self.output_path, class_function_name + title + ".csv"])
        # lower columns
        df.columns = df.columns.str.lower()
        df.to_csv(full_output_path, index=False)

        self.logger.info(full_output_path + " file saved successfully")

        return None
