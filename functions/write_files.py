import os
from google.genai import types
from functions.helper_funcs import validate_target

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def write_file(working_directory: str, file_path: str, content: str) -> str:
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

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
