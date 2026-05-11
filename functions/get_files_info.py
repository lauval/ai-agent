import os


def get_files_info(working_directory, directory="."):
    """
    Fetch metadata for all items present in a directory of concern.

    Args:
        working_directory (str): the directory to which the agent's actions are
                                 restricted.
        directory (str, optional): the directory the agent wants to explore.
                                   Defaults to ".".

    Returns:
        str: one self-contained string consisting of the file name, size and
             directory status of each item in the target directory
    """
    try:
        # attempt to construct an absolute common path
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
        common_path = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
        
        # now check if the directory argument is a directory
        if not common_path:
            return (
                f'Error: Cannot list "{directory}" as it is outside the '
                f"permitted working directory"
            )

        # iterate over the target dir and return a string of metadata
        list_of_metadata = [
            f"- {dir_entry.name}: file_size={dir_entry.stat().st_size} bytes,"
            f" is_dir={dir_entry.is_dir()}"
            for dir_entry in os.scandir(target_dir)
        ]

        return "\n".join(list_of_metadata)

    except Exception as error:
        return f"Error: {error}"
