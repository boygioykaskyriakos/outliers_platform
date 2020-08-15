import os
from configparser import ConfigParser, RawConfigParser

from static_files.standard_variable_names import MAIN_CONFIG


class ReadIniFile:
    """
    This Class reads the configuration file with .ini format
    """

    # setup the configuration file
    config_file_path = os.path.join(os.getcwd(), MAIN_CONFIG)
    config = ConfigParser()
    config.read(config_file_path)

    @classmethod
    def get_parameter(cls, field_name, parameter_name):
        return cls.config.get(field_name, parameter_name)

    @classmethod
    def get_data_type(cls, parameter_name, data_type):
        if isinstance(parameter_name, data_type):
            return parameter_name
        else:
            return data_type(parameter_name)

    @classmethod
    def get_str(cls, field_name, parameter_name):
        return cls.get_data_type(cls.get_parameter(field_name, parameter_name), str)

    @classmethod
    def get_int(cls, field_name, parameter_name):
        return cls.get_data_type(cls.get_parameter(field_name, parameter_name), int)

    @classmethod
    def get_float(cls, field_name, parameter_name):
        return cls.get_data_type(cls.get_parameter(field_name, parameter_name), float)

    @classmethod
    def get_boolean(cls, field_name, parameter_name):
        return cls.config.getboolean(field_name, parameter_name)
