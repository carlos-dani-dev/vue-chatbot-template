from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Json


class CreateUserRequest(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    password: str
    role: str


class GetToken(BaseModel):
    access_token: str
    token_type: str

class ChatSession(BaseModel):
    id: UUID
    user_id: UUID
    tittle: str
    created_at: datetime
    metadata: Json

    class Config:
        from_attributes=True


class ChatMessage(BaseModel):
    id: UUID
    session_id: UUID
    sender: str
    message: str
    timestamp: datetime
    tokens_input: int
    tokens_output: int
    metadata: Json
    
    class Config:
        from_attributes=True