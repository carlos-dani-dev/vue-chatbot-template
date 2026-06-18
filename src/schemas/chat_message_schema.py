from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any, Literal

MessageRole = Literal["system", "user", "assistant", "tool"]


class CreateChatMessageRequest(BaseModel):
    session_id: UUID
    sender: str
    message: str
    timestamp: datetime
    tokens_input: int
    tokens_output: int
    
    class Config:
        from_attributes=True


class ChatMessage(BaseModel):
    chat_session_id: UUID
    role: MessageRole
    content: str
    created_at: datetime


class MessageListResponse(BaseModel):
    chat_session_id: UUID
    list_messages: list[ChatMessage]


class SendChatMessageResponse(BaseModel):
    chat_session_id: str
    user_message: ChatMessage
    assistant_message: ChatMessage
    latency_ms: int
    context_window_size: int
    ctxt_strategy: str = Field(description="Estratégia de contexto utilizada nesta requisição (?)")


class SendChatMessageRequest(BaseModel):
    content: str
    model: str
    system_prompt: str | None