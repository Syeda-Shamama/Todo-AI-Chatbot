# Frontend Context

## Overview
Plain HTML/CSS/JS chat UI — no frameworks, no npm, no build step. Communicates with the FastAPI backend via fetch API.

## Files
| File | Purpose |
|---|---|
| `index.html` | Chat UI layout — message list, input box, send button |
| `style.css` | Chat UI styling — clean, minimal chat interface |
| `script.js` | Sends messages to backend, renders responses, manages conversation_id |

## API Integration
- Endpoint: `POST /api/{user_id}/chat`
- Request body:
  ```json
  { "conversation_id": 1, "message": "Add a task to buy groceries" }
  ```
- Response:
  ```json
  { "conversation_id": 1, "response": "Done! I added 'Buy groceries'.", "tool_calls": [...] }
  ```
- `conversation_id` starts as `null` on first message, then stored from response and sent on every subsequent message

## Key Behaviors
- On page load: `conversation_id = null`, `user_id` hardcoded or from URL param
- On send: POST to backend, append user bubble + assistant bubble to chat
- Store `conversation_id` from first response and reuse for the session
- Show loading indicator while waiting for response
- Handle errors gracefully (show error message in chat)

## Important
- No OpenAI ChatKit — this is a custom UI
- No npm, no Node.js, no build tools — just static files
- Backend runs on `http://localhost:8000` during development
- CORS is handled by FastAPI backend
