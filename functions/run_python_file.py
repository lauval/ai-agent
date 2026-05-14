import subprocess
import os
from functions.helper_funcs import validate_target


def run_python_file(working_directory:str, file_path:str, args=None):
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
        completed_process = subprocess.run(exec_command, cwd=working_directory,capture_output=True, timeout=30, text=True)

        output = []
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}.")

        if not completed_process.stderr and not completed_process.stdout:
            output.append("No output produced")
        else:
            output.append(f"STDOUT: {completed_process.stdout}, STDERR: {completed_process.stderr}")
        
        return " ".join(output)
    
    except Exception as e:
        return f"Error: {e}"