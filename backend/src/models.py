import uuid
from datetime import UTC, datetime
from sqlalchemy import Column, Uuid, Integer, DateTime, String, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID]=mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    email: Mapped[str]=mapped_column(String)
    username: Mapped[str]=mapped_column(String)
    hashed_password: Mapped[str]=mapped_column(String, nullable=False)
    role: Mapped[str]=mapped_column(String, nullable=False)

    chat_sessions: Mapped[list["ChatSession"]] = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[uuid.UUID]=mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID]=mapped_column(Uuid, ForeignKey("users.id"), nullable=False)
    title: Mapped[str]=mapped_column(String)
    channel: Mapped[str]=mapped_column(String, default="web")
    created_at: Mapped[datetime]=mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    chat_session_summary: Mapped[str]=mapped_column(String, default="", nullable=True)
    session_metadata: Mapped[dict[str, any]]=mapped_column(JSON)

    user: Mapped["User"]=relationship("User", back_populates="chat_sessions")
    messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage", back_populates="session", cascade="all, delete-orphan", passive_deletes=True
    )

class ChatMessage(Base):
    __tablename__="chat_messages"

    id: Mapped[uuid.UUID]=mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[str]=mapped_column(String, nullable=False)
    content: Mapped[str]=mapped_column(String, nullable=False)
    created_at: Mapped[datetime]=mapped_column(DateTime, nullable=False)

    session: Mapped[list["ChatSession"]]=relationship("ChatSession", back_populates="messages")