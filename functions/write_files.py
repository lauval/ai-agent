import os
from functions.helper_funcs import validate_target


def write_file(working_directory: str, file_path: str, content: str):
    try:
        valid, target = validate_target(working_directory, file_path)
        print(f"\n\nTARGET FILE PATH: {target}")
        if not valid:
            return (
                f'Error: Cannot write to "{file_path}" as it is outside the permitted '
                f"working directory"
            )

        elif os.path.isdir(target):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # create intermediate directories of the file path if they don't already exist
        os.makedirs(os.path.dirname(target), exist_ok=True)

        with open(target, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
