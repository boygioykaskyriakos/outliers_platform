import os
import matplotlib.pyplot as plt


def create_structured_dict(field_1: str, field_2: str, f1_param: int, f2_param: int or float, d_type: str):
    """
    This method returns a structured dictionary that is used in order to visualize the results

    :param field_1: str: key of first field
    :param field_2: str: key of second field
    :param f1_param: int: value of first key
    :param f2_param: numeric: value of second key
    :param d_type: str: type of d_type
    :return: structured dictionary
    """

    dic = {
        field_1: int(f1_param),
        field_2: int(f2_param) if d_type == 'int' else float(f2_param)
    }

    return dic


def print_data(data: dict):
    """
    This method prints the data

    :param data: dict: structured data
    :return: None
    """
    for key, value in data.items():
        if isinstance(value, list):
            print("{}".format(key))
            for v in value:
                print(v)
        else:
            print("{}:{}".format(key, value))

    print("----------------------------------------------------------------------------------")


def save_fig(title: str, path_to_save=""):
    """
    This method saves the plot to a specific path

    :param title: the title of the plot
    :param path_to_save: full path to save the plot
    :return: None
    """
    # if path to save is not defined, then save on a default location
    # check if default path exists and if not create it
    if path_to_save == "":
        dir_path = os.getcwd()
        path_to_save = "/".join([dir_path, 'plots'])
        
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)

    title = title.replace(" ", "_")
    full_path = "/".join([path_to_save, title+'.jpg'])
    plt.savefig(full_path)
    plt.clf()

    return 0


def linear_search_bigger(array: list, compare_parameter: int or float) -> list:
    """
    Τhis method implements the linear search and is returning the indexes of all the elements of the array
    that are bigger from the comparator

    :param array: list: the array of measurements
    :param compare_parameter: int or float: the number to compare with
    :return: list: a list of indexes
    """
    matches = []
    for i in range(len(array)):
        if array[i] >= compare_parameter:
            matches.append(i)
    return matches


def linear_search_smaller(array: list, compare_parameter: int or float) -> list:
    """
        Τhis method implements the linear search and is returning the indexes of all the elements of the array
        that are smaller from the comparator

        :param array: list: the array of measurements
        :param compare_parameter: int or float: the number to compare with
        :return: list: a list of indexes
        """
    matches = []
    for i in range(len(array)):
        if array[i] <= compare_parameter:
            matches.append(i)
    return matches


def linear_search_equals(array: list, compare_parameter: int or float) -> list:
    """
        Τhis method implements the linear search and is returning the indexes of all the elements of the array
        that are equal from the comparator

        :param array: list: the array of measurements
        :param compare_parameter: int or float: the number to compare with
        :return: list: a list of indexes
        """
    matches = []
    for i in range(len(array)):
        if array[i] == compare_parameter:
            matches.append(i)
    return matches


def visualize_results_hist(arr_results: list, title: str, x_label="", y_label="", path_to_save=""):
    """
    This method visualizes the results

    :param arr_results: list: the array to be visualized
    :param title: str: title to be used
    :param x_label: str: the label of x_axis
    :param y_label: str: the label of y_axis
    :param path_to_save: str: the path to save the plot
    :return: None
    """
    plt.hist(arr_results)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    save_fig(title, path_to_save)

    return 0


def visualize_results_simple_plot(x: list, y: list, title: str, x_label="", y_label="", path_to_save="", line=True):
    """
    This functions creates a simple plot

    :param x: x axis data
    :param y: y axis data
    :param title: title of plot
    :param x_label: x_axis caption
    :param y_label: y_axis caption
    :param path_to_save: the path to save the plot
    :return: None
    """
    if line:
        plt.plot(x, y)
    else:
        plt.plot(x, y, 'ro')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    save_fig(title, path_to_save)

    return 0