import os
from google.genai import types
from functions.helper_funcs import validate_target, READ_CHAR_LIMIT

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Call this function when you need to read file contents. Returns up to 10,000 characters "
        "of a specified file relative to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The (relative) path of the file to be read.",
            ),
        },
    ),
)


def get_file_content(working_directory: str, file_path: str) -> str:
    """
    Fetches and returns up to 10,000 characters of a given file if and only if it lives
    within the boundaries of the working directory.
    """
    try:
        valid_target, target_file = validate_target(working_directory, file_path)

        if not valid_target:
            return (
                f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            )
        elif not os.path.isfile(target_file):
            return f"Error: File not found or is not a regular file: {file_path}"

        with open(target_file, "r") as f:
            file_contents = f.read(READ_CHAR_LIMIT)
            if f.read(1):
                file_contents += (
                    f'[...File "{target_file}" truncated at {READ_CHAR_LIMIT} characters]'
                )

        return file_contents

    except Exception as e:
        return f"Error: {e}"
