import os # read env variables
from flask import Flask, request, jsonify 
import time #delay between api calls
from google import genai # client library that talks, format requests to GEMINI and parse responses 
from load_data import load_data 

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@app.route("/analyze", methods=["POST"])

def analyze():

    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "Please provide a question"}), 400

    QUESTION = data["question"]

    files = load_data()
    responses = []

    for file in files:
        PROMPT = f"""
Answer the question using only this information:

{file['content']}

Question: {QUESTION}
"""

        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=PROMPT
        )

        responses.append({
            "file": file["filename"],
            "answer": response.text
        })

    return jsonify({
        "question": QUESTION,
        "results": responses
    })

if __name__ == "__main__":
    app.run(debug=True)
