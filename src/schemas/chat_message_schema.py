from typing import Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class CreateChatMessageRequest(BaseModel):
    session_id: UUID
    sender: str
    message: str
    timestamp: datetime
    tokens_input: int
    tokens_output: int
    message_metadata: dict[str, Any]
    
    class Config:
        from_attributes=True


## openai-like schema contracts

