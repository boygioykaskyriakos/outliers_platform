import abc

from utilities.read_ini_file import ReadIniFile
from utilities.save_to_file import SavePdToCSVFile
from utilities.log_module import Logger

from static_files.standard_variable_names import GLOBALS, OUTPUT_PATH, PRINT_DEBUG


class BaseClassAnalytic(object):
    """
    This is the base class of all the analytics
    It implements class variables common for all instances and common to all derived classes
    """
    read_ini_file_obj = ReadIniFile()
    save_file = SavePdToCSVFile(read_ini_file_obj.get_str(GLOBALS, OUTPUT_PATH))
    print_debug = read_ini_file_obj.get_boolean(GLOBALS, PRINT_DEBUG)
    logger = Logger()

    @abc.abstractmethod
    def run(self, *args):
        raise NotImplementedError("method not implemented")
