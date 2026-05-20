import os
from functions.helper_funcs import validate_target
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description=(
        "Lists the immediate (non-recursive) contents of a directory within the working directory. "
        "Returns one entry per line in the format: '- <name>: file_size=<bytes> bytes, is_dir=<bool>'. "
        "Use this to explore the file system before reading or writing files."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Relative path of the directory to list, from the working directory root. "
                    "Defaults to '.' (the working directory itself). "
                    "Must not resolve to a path outside the working directory."
                ),
            ),
        },
    ),
)


def get_files_info(working_directory: str, directory: str = ".") -> str:
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
        valid_target, target_dir = validate_target(working_directory, directory)

        # now check if the directory argument is a directory
        if not valid_target:
            return (
                f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
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
