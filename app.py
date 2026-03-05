import os # read env variables
import json
from flask import Flask, request, jsonify, render_template
import time #delay between api calls
from google import genai # client library that talks, format requests to GEMINI and parse responses 
from load_data import load_data 

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/")
def home():

    chats = load_chat_history()

    return render_template("index.html", chats=chats)


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
    # Combine all file answers into one text
    combined_answer = ""

    for r in responses:
        combined_answer += f"{r['file']}: {r['answer']}\n\n"

    # Save chat
    save_chat(QUESTION, combined_answer)

    return jsonify({
        "question": QUESTION,
        "results": responses
    })


CHAT_FILE = "chat_history.json"

def save_chat(question, answer):

    # If file doesn't exist, create it
    if not os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "w") as f:
            json.dump([], f)

    # Read existing chats
    with open(CHAT_FILE, "r") as f:
        chats = json.load(f)

    # Add new chat
    chats.append({
        "question": question,
        "answer": answer
    })

    # Save back
    with open(CHAT_FILE, "w") as f:
        json.dump(chats, f, indent=4)

def load_chat_history():
    """
    Loads chat history
    """
    if not os.path.exists(CHAT_FILE):
        return []

    with open(CHAT_FILE, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    app.run(debug=True)
