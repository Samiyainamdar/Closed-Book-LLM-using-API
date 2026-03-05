# LLM Document Question Answering System

This project is a simple document-based Question Answering application built using Python, Flask, and Google’s Gemini API.

The system allows users to ask questions about locally stored documents, and the LLM generates answers strictly based on the provided data. It behaves like a closed-book LLM that does not rely on external internet knowledge.

The application also stores chat history locally so previous conversations can be displayed on the UI.

---

## Features

- Ask questions about local documents
- LLM responses generated using Gemini 2.5 Flash
- Answers restricted to provided document content
- Chat interface with conversation history
- Chat history stored using JSON
- Flask backend with simple frontend UI

---

## Tech Stack

- Python
- Flask
- Google Gemini API
- HTML / JavaScript
- JSON (for chat history storage)

---

## Project Structure


project-folder
│
├── data/ # Documents used as the knowledge base
├── templates/ # HTML frontend
│
├── app.py # Main Flask application
├── load_data.py # Loads and processes documents
├── requirements.txt # Python dependencies
├── README.md
└── .gitignore


---

## How It Works

1. User asks a question from the UI
2. Flask backend receives the request
3. Documents are loaded from the `data` folder
4. Each document is sent to the Gemini API
5. Gemini generates answers based on document content
6. Responses are returned to the UI
7. The question and response are stored in `chat_history.json`

---

## Setup Instructions

### 1. Clone the repository


git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

cd YOUR_REPO_NAME


### 2. Install dependencies


pip install -r requirements.txt


### 3. Set your Gemini API key

Mac/Linux:


export GEMINI_API_KEY="your_api_key_here"


Windows (PowerShell):


setx GEMINI_API_KEY "your_api_key_here"


### 4. Run the application


python app.py


### 5. Open in browser


http://127.0.0.1:5000


---

## Future Improvements

- Implement vector search (RAG) instead of sending all documents to the LLM
- Add document embeddings
- Improve the chat interface
- Store chat history in a database instead of JSON
- Add multi-document retrieval

---

Built as a learning project to understand LLM APIs, document QA systems, and Flask-based AI applications.

## Author
Samiya Inamdar