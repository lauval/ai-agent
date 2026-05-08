import os


def get_files_info(working_directory, directory="."):
    # check if the directory path is inside the working directory
    abs_path_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_path_working_dir, directory))

    # check if the target_dir path falls within the absolute working dir path
    common_path = os.path.commonpath([abs_path_working_dir, target_dir])

    if common_path != working_directory:
        return f'Error: "{directory}" is not a directory'

    # TODO: iterate over all files in directory
    # record file size and whether it's a directory itself
    # return a string representing the contents of the target directory.
    # e.g.
    # - README.md: file_size=1032 bytes, is_dir=False
