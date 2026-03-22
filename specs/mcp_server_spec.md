# MCP Server Specification

## Overview
The MCP server provides a standardized interface for the AI agent to interact with the task database. It exposes tools for creating, listing, updating, completing, and deleting tasks.

## Tools

### `add_task`
- **Purpose**: Create a new task in the database.
- **Parameters**:
  - `user_id` (string, required): Unique identifier for the user.
  - `title` (string, required): Title of the task.
  - `description` (string, optional): Detailed description of the task.
- **Returns**:
  - `task_id` (integer)
  - `status` (string: "created")
  - `title` (string)

### `list_tasks`
- **Purpose**: Retrieve tasks for a specific user.
- **Parameters**:
  - `user_id` (string, required): Unique identifier for the user.
  - `status` (string, optional): Filter by status ("all", "pending", "completed"). Defaults to "all".
- **Returns**:
  - Array of task objects (id, title, description, completed, created_at, updated_at).

### `complete_task`
- **Purpose**: Mark a task as completed.
- **Parameters**:
  - `user_id` (string, required): Unique identifier for the user.
  - `task_id` (integer, required): ID of the task to complete.
- **Returns**:
  - `task_id` (integer)
  - `status` (string: "completed")
  - `title` (string)

### `delete_task`
- **Purpose**: Remove a task from the database.
- **Parameters**:
  - `user_id` (string, required): Unique identifier for the user.
  - `task_id` (integer, required): ID of the task to delete.
- **Returns**:
  - `task_id` (integer)
  - `status` (string: "deleted")
  - `title` (string)

### `update_task`
- **Purpose**: Modify an existing task's title or description.
- **Parameters**:
  - `user_id` (string, required): Unique identifier for the user.
  - `task_id` (integer, required): ID of the task to update.
  - `title` (string, optional): New title for the task.
  - `description` (string, optional): New description for the task.
- **Returns**:
  - `task_id` (integer)
  - `status` (string: "updated")
  - `title` (string)

## Error Handling
- Return clear error messages if a task is not found.
- Handle database connection errors gracefully.
