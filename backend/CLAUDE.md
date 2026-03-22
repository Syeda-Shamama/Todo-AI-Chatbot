# Backend Context

## Overview
Python FastAPI backend. Handles the chat endpoint, runs the Groq-powered agent, hosts the MCP server, and persists all state to Neon PostgreSQL via SQLModel.

## Virtual Environment
- Located at `backend/venv/`
- Activate on Windows: `venv\Scripts\activate`
- Install deps: `pip install -r requirements.txt`

## Dependencies (requirements.txt)
- `fastapi` — web framework
- `uvicorn` — ASGI server
- `sqlmodel` — ORM (wraps SQLAlchemy + Pydantic)
- `mcp` — Official MCP Python SDK
- `groq` — Groq Python SDK for AI calls
- `python-dotenv` — load `.env` file

## File Responsibilities
| File | Purpose |
|---|---|
| `models.py` | SQLModel table definitions: Task, Conversation, Message |
| `database.py` | DB engine creation, session dependency, create_all tables |
| `mcp_server.py` | MCP server with 5 tools: add_task, list_tasks, complete_task, delete_task, update_task |
| `agent.py` | Groq agent logic — builds message history, calls Groq API with MCP tools, returns response |
| `main.py` | FastAPI app — defines `POST /api/{user_id}/chat`, orchestrates agent + DB persistence |
| `.env` | GROQ_API_KEY, DATABASE_URL (never commit this file) |

## Database Models (models.py — already created)
- `Task` — user_id, id, title, description, completed, created_at, updated_at
- `Conversation` — user_id, id, created_at, updated_at, messages[]
- `Message` — user_id, id, conversation_id, role (user/assistant), content, created_at

## MCP Tools (to implement in mcp_server.py)
All tools receive `user_id` and interact with DB:
1. `add_task(user_id, title, description?)` → returns task_id, status, title
2. `list_tasks(user_id, status?)` → returns array of tasks
3. `complete_task(user_id, task_id)` → returns task_id, status, title
4. `delete_task(user_id, task_id)` → returns task_id, status, title
5. `update_task(user_id, task_id, title?, description?)` → returns task_id, status, title

## Chat Endpoint (main.py)
```
POST /api/{user_id}/chat
Request:  { conversation_id?: int, message: string }
Response: { conversation_id: int, response: string, tool_calls: array }
```

## Conversation Flow
1. Receive user message
2. Fetch conversation history from DB (or create new conversation)
3. Store user message in DB
4. Run Groq agent with history + MCP tools
5. Store assistant response in DB
6. Return response to client

## Groq Model to Use
- `llama-3.3-70b-versatile` — free tier, supports function/tool calling
- Fallback: `llama3-8b-8192` (faster, smaller)

## Important
- Never import or use `openai` package — use `groq` SDK only
- All DB operations use SQLModel sessions from `database.py`
- MCP server runs in-process (not as a separate process)
