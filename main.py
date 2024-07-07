import os
import re
import time
# import memory_profiler
import numpy as np
import google.generativeai as genai

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
            output = run_external_code(code, sample_data)
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
            f"2. Your task is to Generate 10 ready-to-run Python unit tests for the provided code, without comments and descriptions:\n{python_code}\n"
            f"1. The test would be using assertNotEqual instead of assertEqual for the all of the test cases."
            f"4. Make sure the comparison between expected and actual output is done using same data types."
            f"3. Before each variation, I want you to think through what a good header would be and elaborate on your reasoning before you write out the unit test."
            f"5. Generate the test as mentioned above."
            )
        
        unit_test_response = chat.send_message(unit_test_query)
        unit_tests =  unit_test_response.text

        # Generated test handling, disable when generating unit tests with comment and description
        # Removing "``` python" "\\n" etc. human readable description
        unit_tests = massageOutput(unit_tests)

        # Generate metrics
        ## Execution time
        # start_time = time.time()
        # result = my_function(data)
        # end_time = time.time()

        # execution_time = end_time - start_time

        ## Memory usage
        # memory_usage = memory_profiler.memory_usage()[0]

        ## Code Coverage
        # import coverage

        # cov = coverage.Coverage()
        # cov.start()

        # # Your code here (including all functions you want to test)

        # cov.stop()
        # cov.report()  # Prints line and branch coverage statistics

        # # Optionally, generate an HTML report
        # cov.html_report(directory='coverage_report') 



        # Generate code quality metrics, such as cyclomatic complexity and maintainability index.
        # Analyze the code for potential security vulnerabilities and suggest improvements.
        # Evaluate the code for performance bottlenecks and suggest optimizations.


        # Generate suggestions


        #TODO:
        ## Billy
        ### 1. Integrate the extracted function to run and validate each unit test
        ### 2. extract the tests from llm output
        ### 3. Most likely will need to reuse the string code extraction to run the unit tests
        ### 4. Only output the passed unit tests

        ## Sebastian
        ### 1. Implement the rest of the metrics generation
        ### 2. Implement the suggestions generation


        response = {
            "sample_data": sample_data,
            "validation_result": validation_result,
            "unit_tests": unit_tests,
            "metrics": {
                "execution_time": execution_time
            },
            "suggestions": []
        }

        return jsonify(response)


    except ValueError as e:
        return jsonify({"error": "Invalid input.", "details": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500

def massageOutput(input: str):
    input = input.replace("\\n", "")
    input = input.replace("\n", " ")
    input = input.replace("```python", " ")
    input = input.replace("```", " ")

    return input

def extract_function_name(code):
    function_name_match = re.search(r'def\s+(\w+)\s*\(', code)
    if function_name_match:
        return function_name_match.group(1)
    else:
        return None
    
def run_external_code(string_code, data):
    function_name = extract_function_name(string_code)

    if function_name is None:
        raise ValueError("Missing function name. i.e. def my_function(data):")
    
    # Execute the function definition
    exec(string_code)
        
    # Call the function dynamically
    start_time = time.time()
    result = eval(f'{function_name}({data})')
    end_time = time.time()
    execution_time = end_time - start_time

    output = {}
    output["results"] = result
    output["execution_time"] = execution_time
    return output

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