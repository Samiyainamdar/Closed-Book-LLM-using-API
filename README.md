# Closed Book LLM

A Flask-based AI system that answers questions **strictly from local documents** instead of external knowledge.  
The application uses Google's Gemini model but restricts responses to provided file content.

---

## Features

- Closed-book LLM querying
- Gemini API integration
- Multi-document analysis
- User authentication (Signup/Login)
- Password hashing for security
- Session-based access control
- Persistent chat history
- Simple interactive web interface

---

## Tech Stack

Backend
- Python
- Flask

AI
- Google Gemini API

Frontend
- HTML
- CSS
- JavaScript (Fetch API)

Security
- Werkzeug password hashing
- Flask session authentication

---

## Project Structure


closed-book-llm/
│
├── app.py
├── load_data.py
├── users.json
│
├── chat_history/
│
├── templates/
│ ├── index.html
│ ├── login.html
│ └── signup.html
│
└── README.md


---

## Installation

### 1 Install dependencies

```bash
pip install flask google-genai werkzeug
2 Set Gemini API Key

Linux / Mac

export GEMINI_API_KEY=your_api_key

Windows

set GEMINI_API_KEY=your_api_key
3 Run the application
python app.py

Open in browser:

http://127.0.0.1:5000
How It Works

User signs up or logs in

User asks a question

Server loads local documents

Each document is sent to Gemini

Gemini generates answers only using that content

Results are returned and stored as chat history

Example Query

User:

What does this document say about machine learning?

Response:

[file1.txt]
Answer generated from document content...
Future Improvements

Vector database (FAISS / Chroma)

Embedding-based retrieval (RAG)

Streaming LLM responses

ChatGPT-style UI

Cloud deployment

Author

Samiya Inamdar