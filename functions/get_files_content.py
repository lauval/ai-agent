import os
from functions.helper_funcs import validate_target, READ_CHAR_LIMIT


def get_file_content(working_directory: str, file_path: str):
    """
    Fetches and returns up to 10,000 characters of a given file if and only if it lives
    within the boundaries of the working directory.
    """
    try:
        valid_target, target_file = validate_target(working_directory, file_path)

        if not valid_target:
            return (
                f'Error: Cannot read "{file_path}" as it is outside the '
                f"permitted working directory"
            )
        elif not os.path.isfile(target_file):
            return f"Error: File not found or is not a regular file: {file_path}"

        with open(target_file, "r") as f:
            file_contents = f.read(READ_CHAR_LIMIT)
            if f.read(1):
                file_contents += (
                    f'[...File "{target_file}" truncated at '
                    f"{READ_CHAR_LIMIT} characters]"
                )

        return file_contents

    except Exception as e:
        return f"Error: {e}"
