from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: str


class CreateUserResponse(BaseModel):
    email: EmailStr
    username: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
