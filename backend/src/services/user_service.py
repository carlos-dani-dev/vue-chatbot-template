import uuid

from typing import Annotated

from datetime import timedelta, datetime, timezone
from ..config import SECRET_KEY, ALGORITHM

import bcrypt
from jose import JWTError, jwt

from sqlalchemy.orm import Session
from ..database import SessionLocal

from starlette import status
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from ..models import User
from ..repository.user_repository import UserRepository

if not SECRET_KEY: raise RuntimeError("SECRET_KEY não foi carregada corretamente")

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()


def hash_password(password:str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_pwd:str, hashed_pwd:str):
    return bcrypt.checkpw(plain_pwd.encode('utf-8'), hashed_pwd.encode('utf-8'))


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


class UserService:

    def __init__(self, db):
        self.db = db
        self.repo = UserRepository(db)
    
    async def create_access_token(self, user_id:str, username:str, role:str, expires_delta:timedelta):
        expires = datetime.now(timezone.utc) + expires_delta
        encoded_access_token = jwt.encode(
            {"username":username, "user_id":str(user_id), "role":role, "exp":expires},
            SECRET_KEY, ALGORITHM
        )
        return encoded_access_token


    async def authenticate_user(self, username:str, password:str):
        user = self.repo.get_user_by_username(username)
        if not user: return False
        if not verify_password(password, user.hashed_password): return False
        return user

    async def create_user(
        self, username: str,
        email: str,
        hashed_password: str,
        role: str
    ) -> User:
        return self.repo.create_user(str(uuid.uuid4()), username, email, hashed_password, role)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        username = payload.get("username")
        role = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Impossível validar usuário.")

        user_model = UserRepository(db).get_user_by_id(user_id)
        if user_model is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado.")

        return {"user_id": user_id, "username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Impossível validar usuário.")