import os # read env variables
import json
from flask import Flask, request, jsonify, render_template, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import time #delay between api calls
from google import genai # client library that talks, format requests to GEMINI and parse responses 
from load_data import load_data 

app = Flask(__name__)
app.secret_key = "supersecretkey"

USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return []

    with open(USER_FILE, "r") as f:
        return json.load(f)


def save_user(username, password):
    users = load_users()

    users.append({
        "username": username,
        "password": generate_password_hash(password)
    })

    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        for user in users:
            if user["username"] == username:
                return "User already exists"

        save_user(username, password)

        return redirect("/login")

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        for user in users:
            if user["username"] == username and check_password_hash(user["password"], password):
                session["user"] = username
                return redirect("/")

        return "Invalid credentials"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/")
def home():

    if "user" not in session:
        return redirect("/login")

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

CHAT_FOLDER = "chat_history"

if not os.path.exists(CHAT_FOLDER):
    os.makedirs(CHAT_FOLDER)

def save_chat(question, answer):

    username = session["user"]
    chat_file = os.path.join(CHAT_FOLDER, f"{username}.json")

    chats = []

    if os.path.exists(chat_file):
        with open(chat_file, "r") as f:
            chats = json.load(f)

    chats.append({
        "question": question,
        "answer": answer
    })

    with open(chat_file, "w") as f:
        json.dump(chats, f, indent=4)

def load_chat_history():

    if "user" not in session:
        return []

    username = session["user"]
    chat_file = os.path.join(CHAT_FOLDER, f"{username}.json")

    if not os.path.exists(chat_file):
        return []

    with open(chat_file, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    app.run(debug=True)
