from functions.write_files import write_file

test_cases = [
    ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
    ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    ("calculator", "/tmp/temp.txt", "this should not be allowed"),
]


# wrapper function to test get_files_info
def test_write_file(working_directory: str, file_path: str, content: str) -> str:
    result = write_file(working_directory, file_path, content)

    return f"\nResult for {file_path} in working directory: {working_directory}, file:\n{result}"


all_test_cases = list(map(lambda tup: test_write_file(tup[0], tup[1], tup[2]), test_cases))

print("\n\n".join(all_test_cases))
