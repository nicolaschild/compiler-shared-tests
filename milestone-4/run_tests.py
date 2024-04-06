import os

def run_tests() -> None:
    # Get the files in ./tests
    test_files = os.listdir('./tests')
    # Filter out the files that don't end with .kxi
    test_files = [f for f in test_files if f.endswith('.kxi')]
    #Open the file
    for test_file in test_files:
        with open(f'./tests/{test_file}', 'r') as file:
            print(f'Running test {test_file}')
            # For each file, split on the triple dash ---
            file_str = file.read()
            tests = file_str.split('---')
            test_file = tests[0] ; expected_output = tests[1]
            print(test_file, expected_output)


if __name__ == '__main__':
    run_tests()