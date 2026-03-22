# Todo AI Chatbot — Root Context

## Project Overview
An AI-powered chatbot for managing todos through natural language. The AI agent uses MCP (Model Context Protocol) tools to interact with tasks, and persists conversation state to a database so the server remains stateless.

## Tech Stack
| Component | Technology |
|---|---|
| Frontend | Plain HTML/CSS/JS chat UI |
| Backend | Python FastAPI |
| AI Model | Groq (free tier) |
| AI Framework | Groq Python SDK (no OpenAI, no OpenAI Agents SDK) |
| MCP Server | Official MCP Python SDK |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL (free tier) |

## Directory Structure
```
todo-AI-chatbot/
├── backend/      # FastAPI app, Groq agent, MCP server, DB models
├── frontend/     # Plain HTML/CSS/JS chat UI
├── specs/        # Spec files for MCP tools and agent behavior
├── AGENTS.md     # Pre-written code references
├── README.md     # Full project requirements
└── architecture.md  # Folder/file structure and request flow
```

## Key Rules
- **No OpenAI** — use Groq SDK only for AI calls
- **No paid services** — all tools and APIs must have a free tier
- **Stateless server** — all state (conversations, messages, tasks) lives in the DB
- **MCP-only tool access** — the agent must call MCP tools to manage tasks, never raw DB queries directly
- **Single chat endpoint** — `POST /api/{user_id}/chat`

## Environment Variables
Stored in `backend/.env`:
- `GROQ_API_KEY` — from console.groq.com (free)
- `DATABASE_URL` — Neon PostgreSQL connection string (free tier)
