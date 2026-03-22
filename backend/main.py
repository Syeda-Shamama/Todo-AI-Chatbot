# backend/main.py
# Task: TASK-005 | Spec: REQ-04
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from models import Conversation, Message, User
from agent import run_agent
from auth import hash_password, verify_password, create_access_token, get_current_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AuthRequest(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: list


@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(request: AuthRequest, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.username == request.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    user = User(username=request.username, hashed_password=hash_password(request.password))
    session.add(user)
    session.commit()
    return {"message": "Account created successfully"}


@app.post("/login")
def login(request: AuthRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == request.username)).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, session: Session = Depends(get_session), current_user: str = Depends(get_current_user)):
    user_id = current_user
    # Get or create conversation
    if request.conversation_id:
        conversation = session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # Fetch conversation history
    history = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
    ).all()

    # Build message array for agent
    agent_messages = [
        {"role": msg.role, "content": msg.content}
        for msg in history
    ]
    agent_messages.append({"role": "user", "content": request.message})

    # Store user message
    user_message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content=request.message,
    )
    session.add(user_message)
    session.commit()

    # Run agent
    result = await run_agent(user_id=user_id, messages=agent_messages)

    # Store assistant response
    assistant_message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="assistant",
        content=result["response"],
    )
    session.add(assistant_message)
    session.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        response=result["response"],
        tool_calls=result["tool_calls"],
    )
