import uuid
from sqlalchemy import Column, Uuid, Integer, DateTime, String, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id=Column(Uuid, primary_key=True, default=uuid.uuid4)
    email=Column(String)
    username=Column(String)
    hashed_password=Column(String, nullable=False)
    role=Column(String, nullable=False)

    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id=Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id=Column(Uuid, ForeignKey("users.id"), nullable=False)
    title=Column(String)
    created_at=Column(DateTime)
    session_metadata=Column(JSON)

    user=relationship("User", back_populates="chat_sessions")
    messages=relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__="chat_messages"

    id=Column(Uuid, primary_key=True, default=uuid.uuid4)
    session_id=Column(Uuid, ForeignKey("chat_sessions.id"), nullable=False)
    sender=Column(String, nullable=False)
    message=Column(String, nullable=False)
    timestamp=Column(DateTime, nullable=False)
    tokens_input=Column(Integer, nullable=False)
    tokens_output=Column(Integer, nullable=False)
    message_metadata=Column(JSON)

    session=relationship("ChatSession", back_populates="messages")