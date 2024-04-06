import pytest
import sys
import os

def run_tests():
    # Get the files in ./tests
    test_files = os.listdir('./tests')
    # Filter out the files that don't end with .kxi
    test_files = [f for f in test_files if f.endswith('.kxi')]
    #Open the file
    with open('test_results.txt', 'w') as f:
        # For each file, split on the triple dash ---
        string = file.read()
        tests = string.split('---')
        test_file = tests[0]
        expected_output = tests[1]