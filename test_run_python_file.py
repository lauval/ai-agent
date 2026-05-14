from functions.run_python_file import run_python_file

test_cases = [
    ("calculator", "main.py"),
    ("calculator", "tests.py"),
    ("calculator", "../main.py"),
    ("calculator", "nonexistent.py"),
    ("calculator", "lorem.txt")
]

special_cases = [
    ("calculator", "main.py", "3 + 5")
]


# wrapper function to test get_files_info
def test_run_python_file(working_directory, file_path, *args):
    result = run_python_file(working_directory, file_path, args)

    return f"\nResult for {file_path} in working directory: {working_directory}, file:\n{result}"


all_test_cases = list(
    map(lambda tup: test_run_python_file(tup[0], tup[1]), test_cases)
)
special_case = list(
    map(lambda tup: test_run_python_file(tup[0], tup[1], tup[2]), special_cases)
)

print("\n\n".join(all_test_cases))

print("\n".join(special_case))
