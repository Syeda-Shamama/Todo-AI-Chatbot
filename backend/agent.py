# backend/agent.py
# Task: TASK-004 | Spec: REQ-03
import os
import re
import json
from datetime import datetime
from groq import Groq, BadRequestError
from dotenv import load_dotenv
from mcp_server import (
    add_task, list_tasks, complete_task, delete_task, update_task
)

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"

# MCP tools exposed to the Groq agent as function definitions
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Optional task description"},
                },
                "required": ["user_id", "title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Retrieve tasks for the user, optionally filtered by status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter tasks by status",
                    },
                },
                "required": ["user_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "task_id": {"type": "integer", "description": "The task ID to complete"},
                },
                "required": ["user_id", "task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task from the list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "task_id": {"type": "integer", "description": "The task ID to delete"},
                },
                "required": ["user_id", "task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update a task's title or description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The user ID"},
                    "task_id": {"type": "integer", "description": "The task ID to update"},
                    "title": {"type": "string", "description": "New title"},
                    "description": {"type": "string", "description": "New description"},
                },
                "required": ["user_id", "task_id"],
            },
        },
    },
]

# Map tool names to MCP functions
TOOL_FUNCTIONS = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
    "update_task": update_task,
}

SYSTEM_PROMPT_TEMPLATE = """You are a helpful todo assistant. You help users manage their tasks through natural language.
The current user's ID is: {user_id}. Always use this exact user_id when calling tools.
Always use the available tools to perform task operations. After each tool call, confirm the action with a friendly response.
Handle errors gracefully and inform the user if something goes wrong.

Important rules:
- For update_task: NEVER invent or assume a new title or description. If the user has not provided the new title or description, ask them first before calling the tool.
- For complete_task or delete_task: if the user does not mention a task ID and there are multiple tasks, list the tasks first and ask which one they mean.
- Never make up data — only use what the user explicitly tells you."""


async def run_agent(user_id: str, messages: list) -> dict:
    """
    Run the Groq agent with conversation history.
    Returns the assistant response and list of tool calls made.
    """
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(user_id=user_id)
    agent_messages = [{"role": "system", "content": system_prompt}] + messages
    tool_calls_made = []

    while True:
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=agent_messages,
                tools=TOOLS,
                tool_choice="auto",
            )
        except BadRequestError:
            # Retry without tools — handles simple messages and model tool-call failures
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=agent_messages,
                )
            except BadRequestError:
                return {
                    "response": "I had trouble processing that request. Could you rephrase it?",
                    "tool_calls": tool_calls_made,
                }

        message = response.choices[0].message

        # No tool call — final response
        if not message.tool_calls:
            clean = re.sub(r'<function[^>]*>.*?</function>', '', message.content or '', flags=re.DOTALL).strip()
            return {
                "response": clean,
                "tool_calls": tool_calls_made,
            }

        # Append assistant message with tool calls
        agent_messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in message.tool_calls
            ],
        })

        # Execute each tool call via MCP functions
        for tool_call in message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            args["user_id"] = user_id  # ensure user_id is always the authenticated one

            fn = TOOL_FUNCTIONS.get(name)
            if fn:
                result = await fn(**args)
            else:
                result = {"error": f"Unknown tool: {name}"}

            tool_calls_made.append({"tool": name, "args": args, "result": result})

            agent_messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, default=lambda o: o.isoformat() if isinstance(o, datetime) else str(o)),
            })
