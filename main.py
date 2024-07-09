import os
import re
import time
# import memory_profiler
import numpy as np
import google.generativeai as genai
import unittest
import io
import sys
import coverage
import json

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    try:
        # Extract and validate input
        data = request.json
        api_key = data.get("apiKey")
        code = data.get("code")
        input_data = data.get("data", {})
        input_type = input_data.get("inputType")
        boundary = input_data.get("boundary")
        result = data.get("result", {})
        expected_output = result.get("expectedOutput")

        # https://platform.openai.com/docs/guides/prompt-engineering/tactic-use-code-execution-to-perform-more-accurate-calculations-or-call-external-apis
        python_code = f"```python\n{code}\n```"

        model = configure_model(api_key)
        chat = model.start_chat(history=[])

        if not api_key or not code or not input_type or not boundary or not expected_output:
            raise ValueError("Missing required fields in the input.")

        # Validate Python syntax
        syntax_check = chat.send_message("Analyze the following Python code snippet and identify any potential syntax errors."
                                         "Do not include indentation and missing imports errors.\n"
                                         f"{python_code}\n"
                                         "Your response should be a simple 'Yes' if no syntax errors or 'No' if there are syntax errors.")
        
        if "No" in syntax_check.text:
            syntax_errors = chat.send_message("List the previous syntax errors in bullet points")
            raise ValueError("Invalid Python syntax:", syntax_errors.text)
            
        # Generate sample data
        sample_data_query = (
            f"Generate diverse testing input data for a Python program that utilizes Flask's jsonify function."
            f"Given the following Python code:\n{python_code}\n"
            f"Following the provided input format type: {input_type}. With the boundary condition being: {boundary}"
            f"The desired output response is a Flask-compatible JSON list containing at least 20 diverse items."
        )

        try:
            sample_data_response = chat.send_message(sample_data_query)
            partitioned_text = sample_data_response.text.partition("```json")[2].partition("```")[0]
            sample_data = eval(partitioned_text)
        except AttributeError:
            sample_data = []

        # Validate the output
        validation_result = ""
        execution_time = 0
        if (len(sample_data) > 0):
            output = test_main_function(code, sample_data)
            result = output["results"]

            validation_query = (
                f"Check each of the results in the following list and determine if they match the expected output:\n{result}\n"
                f"The desired output response is a text, describing if the output is as expected."
            )

            execution_time = output["execution_time"]

            try:
                validation_response = chat.send_message(validation_query)
                validation_result = validation_response.text.replace("\n", "").replace("*", "").strip()
            except AttributeError:
                validation_result = "Generated data validation failed."

        # Generate unit tests
        unit_test_query = (
            f"Generate 5 correct and ready-to-run Python unit tests following the unittest framework for the provided code, without comments and descriptions:\n{python_code}\n"
            f"Make sure the generated test use the same data types as the expected output."
            f"Include the unittest.main() command at the end of the unit test."
            f"Before each variation, I want you to think through if the expected output will match with actual output before you write out the unit test. Update the expected output if necessary."
        )
        
        unit_test_response = chat.send_message(unit_test_query)

        unit_test_response = unit_test_response.text.partition("```python")[2].partition("```")[0]
        
        # Evaluate the generated unit tests
        passed_tests, failed_tests = run_tests(unit_test_response)
        # coverage = run_tests_and_get_coverage(unit_test_response)

        # Generate metrics
        ## Memory usage
        # memory_usage = memory_profiler.memory_usage()[0]


        # Generate code quality metrics, such as cyclomatic complexity and maintainability index.
        # Analyze the code for potential security vulnerabilities and suggest improvements.
        # Evaluate the code for performance bottlenecks and suggest optimizations.


        # Generate suggestions


        ## Sebastian
        ### 1. Implement the rest of the metrics generation
        ### 2. Implement the suggestions generation


        response = {
            "sample_data": sample_data,
            "validation_result": validation_result,
            "unit_tests": {
                "passed_tests": passed_tests,
                "failed_tests": failed_tests
            },
            "metrics": {
                "execution_time": execution_time,
                "coverage": 0,
                "memory_usage": 0
            },
            "suggestions": []
        }

        return jsonify(response)


    except ValueError as e:
        return jsonify({"error": "Invalid input.", "details": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500

def extract_function_name(code):
    function_name_match = re.search(r'def\s+(\w+)\s*\(', code)
    if function_name_match:
        return function_name_match.group(1)
    else:
        return None

def test_main_function(string_code, data):
    start_time = time.time()
    result = run_external_code(string_code, data)
    end_time = time.time()
    execution_time = end_time - start_time

    output = {}
    output["results"] = result
    output["execution_time"] = execution_time
    return output

    
def run_external_code(string_code, data):
    function_name = extract_function_name(string_code)

    if function_name is None:
        raise ValueError("Missing function name. i.e. def my_function(data):")
    
    # Execute the function definition
    exec(string_code)
        
    # Call the function dynamically
    result = eval(f'{function_name}({data})')

    return result

class CustomTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.passed = []
        self.failed = []
    
    def addSuccess(self, test):
        super().addSuccess(test)
        self.passed.append(test)
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.failed.append(test)

def get_test_code(test_case, unit_test_code):
    # Extract the method name
    method_name = test_case._testMethodName
    # Find the method in the unit test code
    lines = unit_test_code.strip().split('\n')
    start_index = None
    end_index = None

    for i, line in enumerate(lines):
        if line.strip().startswith(f'def {method_name}('):
            start_index = i
            break

    if start_index is not None:
        for i in range(start_index + 1, len(lines)):
            if lines[i].strip().startswith('def ') or lines[i].strip().startswith('class ') or lines[i].strip().startswith('if __name__ =='):
                end_index = i
                break

        if end_index is None:
            end_index = len(lines)

    if start_index is not None:
        extracted_lines = lines[start_index:end_index]
        # Left-strip only the first line
        extracted_lines[0] = extracted_lines[0].lstrip()
        return '\n'.join(extracted_lines)
    
    return None

def run_tests(unit_test_code):
    # Create a new module to hold the dynamically generated test cases
    test_module = type(sys)('test_module')
    exec(unit_test_code, test_module.__dict__)

    # Redirect result to capture the test output
    test_output = io.StringIO()
    runner = unittest.TextTestRunner(stream=test_output, verbosity=2, resultclass=CustomTestResult)

    # Load the tests from the dynamically created module
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_module)

    # Run the tests
    result = runner.run(suite)

    # Parse the results
    # NOTE: Use result.failed in local development, if you want to see the failed tests or result.passed is empty
    passed_tests = [get_test_code(test, unit_test_code) for test in result.passed]
    failed_tests = [get_test_code(test, unit_test_code) for test in result.failed]
    
    return passed_tests, failed_tests

def run_tests_and_get_coverage(unit_test_code):
    cov = coverage.Coverage()
    cov.start()

    # Create a new module to hold the dynamically generated test cases
    coverage_module = type(sys)('coverage_module')
    exec(unit_test_code, coverage_module.__dict__)

    cov.stop()
    cov.save()

    print('save')

    cov.json_report(outfile='coverage.json')

    coverage_json = 'No data was collected'

    print('coverage_json')
    if os.path.exists('coverage.json'):
        print('exists')
        with open('coverage.json', 'r') as f:
            coverage_json =json.dumps(json.load(f), indent=2)

    return coverage_json

def configure_model(api_key: str):
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings=safety_settings
    )

    return model



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))