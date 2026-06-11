from typing import Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Json


class ChatSessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    session_metadata: dict[str, Any]

    class Config:
        from_attributes=True


class CreateChatSessionRequest(BaseModel):
    title: str
    session_metadata: dict[str, Any]

class ChatSessionListResponse(BaseModel):
    items: list[ChatSessionResponse]

class ChatMessage(BaseModel):
    id: UUID
    session_id: UUID
    sender: str
    message: str
    timestamp: datetime
    tokens_input: int
    tokens_output: int
    message_metadata: dict[str, Any]
    
    class Config:
        from_attributes=True