import os
from google.genai import types
from functions.helper_funcs import validate_target

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes text content to a file within the working directory, creating the file (and any "
        "missing parent directories) if they do not exist, or replacing the file entirely if it "
        "does. Use this to create new files or overwrite existing ones."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Relative path of the file to write, from the working directory root. "
                    "Parent directories are created automatically if they do not exist."
                ),
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The complete text content to write. Replaces the entire existing file "
                    "content — this is not an append operation."
                ),
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
