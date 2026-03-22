# Agent Behavior Specification

## AI Model
- Provider: Groq (free tier)
- Model: `llama-3.3-70b-versatile` (supports tool/function calling)
- Fallback: `llama3-8b-8192`

## Behavior Rules

| Behavior | Description |
|---|---|
| Task Creation | When user mentions adding/creating/remembering something, use `add_task` |
| Task Listing | When user asks to see/show/list tasks, use `list_tasks` with appropriate filter |
| Task Completion | When user says done/complete/finished, use `complete_task` |
| Task Deletion | When user says delete/remove/cancel, use `delete_task` |
| Task Update | When user says change/update/rename, use `update_task` |
| Confirmation | Always confirm actions with a friendly response |
| Error Handling | Gracefully handle task not found and other errors |

## Natural Language Command Mapping

| User Says | Agent Should |
|---|---|
| "Add a task to buy groceries" | Call `add_task` with title "Buy groceries" |
| "Show me all my tasks" | Call `list_tasks` with status "all" |
| "What's pending?" | Call `list_tasks` with status "pending" |
| "Mark task 3 as complete" | Call `complete_task` with task_id 3 |
| "Delete the meeting task" | Call `list_tasks` first, then `delete_task` |
| "Change task 1 to 'Call mom tonight'" | Call `update_task` with new title |
| "I need to remember to pay bills" | Call `add_task` with title "Pay bills" |
| "What have I completed?" | Call `list_tasks` with status "completed" |

## Conversation Flow (Stateless Request Cycle)

1. Receive user message
2. Fetch conversation history from database
3. Build message array for agent (history + new message)
4. Store user message in database
5. Run agent with MCP tools
6. Agent invokes appropriate MCP tool(s)
7. Store assistant response in database
8. Return response to client
9. Server holds NO state — ready for next request

## Chat API Endpoint

```
POST /api/{user_id}/chat

Request:
{
  "conversation_id": 1,   // optional — creates new if not provided
  "message": "string"     // required
}

Response:
{
  "conversation_id": 1,
  "response": "string",
  "tool_calls": []
}
```
