import os


def create_output_path(output_path: str):
    """
    This function gets creates the output dir if doesn't exists
    :param output_path: str : the output path that will be the projects output dir
    :return: None
    """
    if os.path.exists(output_path):
        if os.path.isdir(output_path):
            return output_path
        else:
            raise NotADirectoryError("The output path (dir) given is not a directory please replace it")

    else:
        os.mkdir(output_path)
