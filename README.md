# Setup Instructions — Todo AI Chatbot

## Prerequisites
- Python 3.10+
- A free [Groq API key](https://console.groq.com)
- A free [Neon PostgreSQL](https://neon.tech) database

---

## 1. Clone the Repository

```bash
git clone <your-repo-url>
cd todo-AI-chatbot
```

---

## 2. Backend Setup

### Create & activate virtual environment
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Configure environment variables
Create `backend/.env`:
```
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=your_neon_postgresql_connection_string
```

- **GROQ_API_KEY** — get free key from [console.groq.com](https://console.groq.com)
- **DATABASE_URL** — get from [neon.tech](https://neon.tech) → your project → Connection string

### Run database migration
```bash
python migrate.py
```

### Start the backend server
```bash
uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`

---

## 3. Frontend Setup

No build step needed — plain HTML/CSS/JS.

Open a new terminal:
```bash
cd frontend
python -m http.server 3000
```

Open browser at: `http://localhost:3000`

---

## 4. Using the Chatbot

Example commands:
| Say | Action |
|---|---|
| "Add a task to buy groceries" | Creates a new task |
| "Show me all my tasks" | Lists all tasks |
| "What's pending?" | Lists incomplete tasks |
| "Mark task 3 as complete" | Completes a task |
| "Delete task 2" | Deletes a task |
| "Update task 1, title(New Title)" | Updates a task |
| "What have I completed?" | Lists completed tasks |

---

## 5. API Reference

```
POST http://localhost:8000/api/{user_id}/chat

Request:
{
  "conversation_id": 1,   // optional
  "message": "Show me my tasks"
}

Response:
{
  "conversation_id": 1,
  "response": "Here are your tasks...",
  "tool_calls": [...]
}
```

---

## Project Structure

```
todo-AI-chatbot/
├── backend/
│   ├── models.py        # DB models
│   ├── database.py      # DB connection
│   ├── mcp_server.py    # MCP tools
│   ├── agent.py         # Groq agent
│   ├── main.py          # FastAPI app
│   ├── migrate.py       # DB migration script
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── specs/               # Specification files
```
