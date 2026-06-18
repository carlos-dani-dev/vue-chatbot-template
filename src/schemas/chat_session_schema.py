from datetime import datetime
from typing import Any
from uuid import UUID
from pydantic import BaseModel


class ChatSessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    created_at: datetime
    channel: str
    session_metadata: dict[str, Any]

    class Config:
        from_attributes=True


class CreateChatSessionRequest(BaseModel):
    title: str
    channel: str
    chat_id: UUID
    session_metadata: dict[str, Any]


class ChatSessionListResponse(BaseModel):
    items: list[ChatSessionResponse]