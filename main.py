import os
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

        model = configure_model(api_key)
        chat = model.start_chat(history=[])


        if not api_key or not code or not input_type or not boundary or not expected_output:
            raise ValueError("Missing required fields in the input.")

        # Validate Python syntax
        syntax_check = chat.send_message(f"Ignore indentation errors and respond with 'Yes' or 'No'. Is this correct Python syntax?\n`{code}`")
        print(syntax_check.text)
        
        if "No" in syntax_check.text:
            syntax_errors = chat.send_message(f"List the syntax errors in bullet points:\n{code}")
            print(syntax_errors.text)
            raise ValueError("Invalid Python syntax:", syntax_errors.text)
        
        # Generate sample data
        sample_data_query = (
            f"Your responses will be used within a python program. You should adapt them so that it can be read by the flask jsonify function.\n"  
            f"Generate relevant testing data for the Python code:\n`{code}`\n"
            f"The input data type should be {input_type} and the boundary should be {boundary}."
            f"Your response should only be a python list (minimum 20 items) of numbered list with the generated data."
        )
        sample_data_response = chat.send_message(sample_data_query)
        sample_data = eval(sample_data_response.text.replace('`', '').replace('python', ''))
        print(sample_data)

        # Edge Case Handling: Generate edge cases for testing, not just typical data.
        # Randomized Data: Use libraries like faker to generate realistic and varied sample data.
        # Custom Data Patterns: Allow users to specify patterns for input data generation

        # Validate the output
        validation_query = (
            f"Run the generated testing data on the code:\n{code}\n"
            f"Are the results as expected? The expected output is {expected_output}."
            f"Display your response as text"
        )

        validation_response = chat.send_message(validation_query)
        validation_result = validation_response.text
        print(validation_result)

        # Generate unit tests
        # unit_test_query = f"Generate ready-to-run Python unit tests for the provided code, including comments and descriptions:\n{code}" # with comment
        unit_test_query = f"Generate ready-to-run Python unit tests for the provided code, without comments and descriptions:\n{code}" # without comment
        unit_test_response = chat.send_message(unit_test_query)
        unit_tests =  unit_test_response.text

        # Generated test handling, disable when generating unit tests with comment and description
        # Removing "``` python" "\\n" etc. human readable description
        unit_tests = massageOutput(unit_tests)

        print(unit_tests)

        # Parameterized Tests: Create parameterized unit tests to handle multiple input scenarios efficiently.
        # Mocking and Patching: Include examples of using unittest.mock to handle external dependencies.
        # Test Coverage: Analyze test coverage and suggest additional test cases to improve it.

        response = {
            "sample_data": sample_data,
            "validation_result": validation_result,
            "unit_tests": unit_tests,
            "metrics": [],  # Metrics can be added here
            "suggestions": [],  # Suggestions can be added here
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

# Gemini LLM call
def callGeminiLLM(apiKey: str, input: str):
    model = configure_model(apiKey)
    chat = model.start_chat(history=[])

    return chat.send_message(input)
       
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