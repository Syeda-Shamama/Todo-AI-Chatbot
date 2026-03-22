# AI Agent Specification

## Overview
The AI Agent is the conversational interface between the user and the task management system. It uses natural language processing to understand user intent and invokes MCP tools to perform actions.

## Behavior Rules

### Task Management
- **Task Creation**: When the user mentions adding, creating, or remembering a task, the agent should call `add_task`.
- **Task Listing**: When the user asks to see, show, or list tasks, the agent should call `list_tasks` with the appropriate status filter.
- **Task Completion**: When the user says a task is done, complete, or finished, the agent should call `complete_task` with the task ID.
- **Task Deletion**: When the user says to delete, remove, or cancel a task, the agent should call `delete_task`.
- **Task Update**: When the user says to change, update, or rename a task, the agent should call `update_task`.

### Interaction Style
- **Friendly and Concise**: The agent should respond in a friendly and helpful manner.
- **Action Confirmation**: After performing an action, the agent must confirm the result (e.g., "Task 'Buy groceries' has been created!").
- **Error Handling**: If a task is not found or an error occurs, the agent should inform the user gracefully and suggest alternatives.

### Conversation Context
- The agent should maintain conversation context across multiple turns using the message history stored in the database.
- It should be able to resolve ambiguous references (e.g., "Delete that task" referring to the last listed task).

## Natural Language Commands Examples
- "Add a task to buy groceries" -> `add_task(title="Buy groceries")`
- "Show me all my tasks" -> `list_tasks(status="all")`
- "What's pending?" -> `list_tasks(status="pending")`
- "Mark task 3 as complete" -> `complete_task(task_id=3)`
- "Delete the meeting task" -> First `list_tasks` to find the ID, then `delete_task(task_id=ID)`.
- "Change task 1 to 'Call mom tonight'" -> `update_task(task_id=1, title="Call mom tonight")`
- "I need to remember to pay bills" -> `add_task(title="Pay bills")`
- "What have I completed?" -> `list_tasks(status="completed")`
