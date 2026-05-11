import os

def make_path_absolute(directory:str):
    """Converts a relative path to absolute

    Args:
        directory (str): the relative path to the directory of concern

    Returns:
        str: the absolute path of the directory of concern
    """
    return os.path.abspath(directory)

def create_target_dir(abs_path_working_dir:str,
                      directory:str):
    """Creates a joint path consisting of the absolute path of the working
    directory plus the directory to grant the agent access to.

    Args:
        abs_path_working_dir (str): the absolute path of the working directory
        directory (str): the (nested) directory to make available to the agent

    Returns:
        str: the normalised joint path 
    """
    # construct the path first, then return the normalised version
    joint_path = os.path.join(abs_path_working_dir, directory)
    return os.path.normpath(joint_path)

def check_path_commonality(paths:list):
    """check whether the absolute paths in a list share some element of their
    paths.

    Args:
        paths (list): list of paths to check for commonality

    Returns:
        bool: True or False depending on whether they share common paths
    """
    return os.path.commonpath(paths)


def get_files_info(working_directory, directory="."):
    # check if the directory path is inside the working directory
    abs_working_dir = make_path_absolute(working_directory)
    target_dir = create_target_dir(abs_working_dir, directory)

    # check if the target_dir path falls within the absolute working dir path   
    common_path = check_path_commonality([abs_working_dir, target_dir])

    if not common_path:
        return f'Error: Cannot list "{target_dir}" as it is outside the permitted working directory'
    
    elif not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'
    
