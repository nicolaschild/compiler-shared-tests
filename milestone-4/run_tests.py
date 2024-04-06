from typing import List
import os, subprocess

# Change this to the path of your run file
PATH_TO_RUN_SH = "../../compiler/compile.sh"
PATH_TO_TESTS = "./tests"

NUM_OF_CORES = os.cpu_count()

# tuple(FILENAME, INPUT, EXPECTED OUTPUT)
def get_tuples() -> List[tuple[str, str, str]]:
    # Get the files in ./tests
    test_files = os.listdir('./tests')
    # Filter out the files that don't end with .kxi
    test_files = [f for f in test_files if f.endswith('.kxi')]
    #Open the file
    all_tests: List[tuple[str, str]] = []
    for test_file in test_files:
        with open(f'./tests/{test_file}', 'r') as file:
            # For each file, split on the triple dash ---
            file_str: str = file.read()
            tests = file_str.split('---')
            test_input: str = tests[0] ; expected_output = tests[1]
            all_tests.append((test_file, test_input, expected_output)) # type: ignore
    return all_tests # type: ignore


def run_parser(test: tuple[str, str, str]) -> tuple[str, str, int]:
    """Save the input string to a file and run the parser"""
    result = subprocess.run(
        [
            test[0],
            "|",
            "python3",
            PATH_TO_RUN_SH,
            "-e",
        
        ],
        text=True,
        capture_output=True,
    )

    return (result.stdout, result.stderr, result.returncode)


def test_desugar_c_minus() -> None:
    test_files = get_tuples()
    for test_file in test_files:
        print(f"Running test {test_file[0]}")
        stdout, stderr, returncode = run_parser(test_file)
        print(stdout)
        print(stderr)
        print(returncode)
        return