from flask import Flask, request, jsonify
import os
import google.generativeai as genai
import re

app = Flask(__name__)


@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    genai.configure(api_key="AIzaSyCkdD4-ui3zBvGg-AE8iJig-54a7ZdVwco")

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=generation_config, safety_settings=safety_settings)
    
    code = request.json["code"]
    inputType = request.json["data"]["inputType"]
    boundary = request.json["data"]["boundary"]
    expectedOutput = request.json["data"]["expectedOutput"]
    
    chat = model.start_chat(history=[])
    response1 = chat.send_message("With a 'Yes' or 'No', is this python code?:" + code)
    if response1.text == "No":
        return "The code provided is not a python code."
    
    response2 = chat.send_message("With a 'Yes' or 'No', is this correct python syntax and can it be run?" + code)
    if response2.text == "No":
        response2_1 = chat.send_message("Highlight what is wrong with the code")
        return f"The code provided is not a correct python syntax. Here are the errors: {response2_1.text}"

    response3 = chat.send_message("Generate a ready to run python unit test for the provided code (without comments and description):" + "only with " + inputType + " cases") 
    response4 = chat.send_message("Create relevant testing data for the python code")

    answer = f"{response3.text}"
    return answer


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))