# Implementation Plan

## Phase 1: Database Setup
- Connect to Neon PostgreSQL using `SQLModel`.
- Create the initial database tables based on the models in `backend/models.py`.

## Phase 2: MCP Server Development
- Use the Official MCP Python SDK.
- Implement each tool defined in `mcp_server_spec.md`.
- Ensure each tool is stateless and interacts with the database directly.

## Phase 3: FastAPI Backend Integration
- Implement the `/api/{user_id}/chat` endpoint.
- Integrate the Groq SDK (llama-3.3-70b-versatile) to handle conversational logic.
- Connect the agent with the MCP server to invoke tools via Groq function calling.
- Set up a stateless request cycle that persists conversation history and messages in the database.

## Phase 4: Frontend
- Build the chat interface using plain HTML/CSS/JS (no frameworks, no build step).
- Ensure the frontend can interact with the `/api/{user_id}/chat` endpoint.
- Store conversation_id from first response and reuse for the session.

## Phase 5: Testing & Deployment
- Write unit tests for MCP tools and the agent's behavior.
- Deploy the frontend and backend.
