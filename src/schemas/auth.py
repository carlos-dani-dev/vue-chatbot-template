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


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
