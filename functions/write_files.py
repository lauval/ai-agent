import os
from google.genai import types
from functions.helper_funcs import validate_target

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Call this function when you need to write contents to a file. You may overwrite the "
        "existing file contents."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The (relative) path of the file to which content will be written",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text that should be written to the target file",
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
