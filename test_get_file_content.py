from functions.get_files_content import get_file_content

test_cases = [
    ("calculator", "lorem.txt"),
    ("calculator", "main.py"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat"),
    ("calculator", "pkg/does_not_exist.py"),
]


# wrapper function to test get_files_info
def test_get_files_content(working_directory, file):
    result = get_file_content(working_directory, file)
    if "lorem" in file and "truncated" in result:
        return f"{file} truncated: True"
    return f"Result for {file} file:\n{result}"


all_test_cases = list(
    map(lambda tup: test_get_files_content(tup[0], tup[1]), test_cases)
)

print("\n\n".join(all_test_cases))
