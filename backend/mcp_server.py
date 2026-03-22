# backend/mcp_server.py
# Task: TASK-003 | Spec: REQ-02
from typing import Optional
from mcp.server.fastmcp import FastMCP
from sqlmodel import Session, select
from database import engine
from models import Task
from datetime import datetime

mcp = FastMCP("todo-mcp-server")

@mcp.tool()
async def add_task(user_id: str, title: str, description: Optional[str] = None):
    """Create a new task for a user."""
    with Session(engine) as session:
        task = Task(user_id=user_id, title=title, description=description)
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"task_id": task.id, "status": "created", "title": task.title}

@mcp.tool()
async def list_tasks(user_id: str, status: Optional[str] = "all"):
    """Retrieve tasks for a user, optionally filtered by status."""
    with Session(engine) as session:
        statement = select(Task).where(Task.user_id == user_id)
        if status == "pending":
            statement = statement.where(Task.completed == False)
        elif status == "completed":
            statement = statement.where(Task.completed == True)
        
        results = session.exec(statement).all()
        return [task.model_dump() for task in results]

@mcp.tool()
async def complete_task(user_id: str, task_id: int):
    """Mark a task as completed."""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return {"error": "Task not found"}
        
        task.completed = True
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"task_id": task.id, "status": "completed", "title": task.title}

@mcp.tool()
async def delete_task(user_id: str, task_id: int):
    """Delete a task."""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return {"error": "Task not found"}
        
        session.delete(task)
        session.commit()
        return {"task_id": task_id, "status": "deleted", "title": task.title}

@mcp.tool()
async def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None):
    """Update a task's title or description."""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return {"error": "Task not found"}
        
        if title:
            task.title = title
        if description:
            task.description = description
        
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"task_id": task.id, "status": "updated", "title": task.title}
