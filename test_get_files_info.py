from functions.get_files_info import get_files_info

test_cases = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../"),
]


# wrapper function to test get_files_info
def test_get_files_info(working_directory: str, directory: str) -> str:
    result = get_files_info(working_directory, directory)
    if directory == ".":
        return f"Result for current directory:\n{result}"
    return f"Result for {directory} directory:\n{result}"


#
all_test_cases = list(map(lambda tup: test_get_files_info(tup[0], tup[1]), test_cases))

print("\n\n".join(all_test_cases))
