import os


def create_output_path(output_path):
    if os.path.exists(output_path):
        if os.path.isdir(output_path):
            return output_path
        else:
            raise NotADirectoryError("The output path given is not a directory please replace it")

    else:
        os.mkdir(output_path)
