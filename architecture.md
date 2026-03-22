# Project Architecture

## Folder & File Structure

```
todo-AI-chatbot/
├── AGENTS.md                  # Pre-written code references
├── README.md                  # Project requirements & specs
├── architecture.md            # This file
│
├── backend/
│   ├── venv/                  # Python virtual environment (not committed)
│   ├── models.py              # SQLModel DB models: Task, Conversation, Message
│   ├── database.py            # DB engine setup & session management (Neon PostgreSQL)
│   ├── mcp_server.py          # MCP server exposing task tools (add, list, complete, delete, update)
│   ├── agent.py               # Groq-powered agent that uses MCP tools to handle user messages
│   ├── main.py                # FastAPI app — POST /api/{user_id}/chat endpoint
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables (GROQ_API_KEY, DATABASE_URL)
│
├── frontend/
│   ├── index.html             # Chat UI layout
│   ├── style.css              # Chat UI styling
│   └── script.js              # Handles sending messages & rendering responses
│
└── specs/
    ├── mcp_tools.md           # Specification for all 5 MCP tools
    └── agent_behavior.md      # Agent behavior rules & natural language command mapping
```

## Request Flow

```
User (frontend)
    │
    │  POST /api/{user_id}/chat
    │  { conversation_id?, message }
    ▼
FastAPI (main.py)
    │
    ├── Fetch conversation history from DB
    ├── Store user message in DB
    │
    ▼
Groq Agent (agent.py)
    │
    ├── Receives: history + new message
    ├── Decides which MCP tool to call
    │
    ▼
MCP Server (mcp_server.py)
    │
    ├── add_task
    ├── list_tasks
    ├── complete_task
    ├── delete_task
    └── update_task
    │
    ▼
Database — Neon PostgreSQL (database.py + models.py)
    │
    ▼
Groq Agent returns response
    │
FastAPI stores assistant response in DB
    │
    ▼
User (frontend) receives:
    { conversation_id, response, tool_calls }
```

## Key Design Principles

- **Stateless server** — no in-memory state; all conversation state lives in the DB
- **MCP tools** — agent interacts with tasks only through MCP tool calls, never raw DB queries
- **Single endpoint** — `POST /api/{user_id}/chat` handles all natural language commands
- **Free stack** — Groq (free tier), Neon PostgreSQL (free tier), no paid services

## Environment Variables (.env)

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Free API key from console.groq.com |
| `DATABASE_URL` | Neon PostgreSQL connection string |
