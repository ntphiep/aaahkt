# Python example with various issues

import os
import subprocess

# Security issues
password = "admin123"  # Hardcoded password
api_key = "sk-1234567890"  # Hardcoded API key

def process_data(user_input):
    # Very dangerous - command injection vulnerability
    result = subprocess.call(user_input, shell=True)
    
    # Multiple nested conditions (high complexity)
    if result == 0:
        if user_input and len(user_input) > 0:
            if user_input.startswith("valid"):
                if user_input.endswith("data"):
                    if "special" in user_input:
                        print("Success")
                        print("Step 1")
                        print("Step 2")
                        print("Step 3")
                        print("Step 4")
                        print("Step 5")
                        print("Step 6")
                        print("Step 7")
    
    # TODO: Fix this security issue
    # FIXME: Refactor this function
    
    # Magic numbers
    value = user_input * 42 + 137 - 256
    another = value / 999 + 12345
    
    return value

def very_long_function_name_that_exceeds_recommended_line_length_and_should_be_refactored():
    return "This function name is way too long"

# No error handling
def risky_operation(filename):
    file = open(filename, 'r')
    data = file.read()
    # File never closed - resource leak
    return data
