import subprocess
import os
from google.genai import types
from functions.helper_funcs import validate_target

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=("Call this function when you need to run python scripts"),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The (relative) path of the python file to be executed",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="This is an optional parameter that accepts lists of strings.",
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory: str, file_path: str, args=None) -> str:
    try:
        valid, target = validate_target(working_directory, file_path)

        if not valid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        elif not os.path.isfile(target):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        elif not target.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        exec_command = ["python", target]

        if args:
            exec_command.extend(args)

        # execute command
        # working dir passed in its absolute form to maintain consistency with `target`
        completed_process = subprocess.run(
            exec_command,
            cwd=os.path.abspath(working_directory),
            capture_output=True,
            timeout=30,
            text=True,
        )

        output = []
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}.")

        if not completed_process.stderr and not completed_process.stdout:
            output.append("No output produced")
        else:
            output.append(f"STDOUT: {completed_process.stdout}")
            output.append(f"STDERR: {completed_process.stderr}")

        return " ".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"
