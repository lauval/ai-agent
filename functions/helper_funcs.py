import os

# constants
READ_CHAR_LIMIT = 10000  # the max number of characters to read from any given file


# functions
def validate_target(
    working_directory: str, directory_or_file_path: str = "."
) -> str | tuple[bool, str]:
    """
    Returns the absolute path of the target directory or file path if and only if it
    shares a common path (lives within) the working directory. Otherwise, it returns an
    error message for the agent, as a string.
    """

    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory_or_file_path))
        target_in_working_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
    except Exception as e:
        return f"Error: {e}"

    return target_in_working_dir, target_dir
