from starlette import status
from typing import Annotated
from pydantic import BaseModel, EmailStr
from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request

import bcrypt
from jose import JWTError, jwt
from ..config import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from sqlalchemy.orm import Session
from ..database import SessionLocal

from ..schemas.auth import CreateUserRequest, TokenResponse
from ..models import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

if not SECRET_KEY: raise RuntimeError("SECRET_KEY não foi carregada corretamente")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


def hash_password(password:str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_pwd:str, hashed_pwd:str):
    return bcrypt.checkpw(plain_pwd.encode('utf-8'), hashed_pwd.encode('utf-8'))


def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()


### endpoints

async def authenticate_user(username:str, password:str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user: return False
    if not verify_password(password, user.hashed_password): return False
    return user

async def create_access_token(user_id:str, username:str, role:str, expires_delta:timedelta):
    expires = datetime.now(timezone.utc) + expires_delta
    encoded_access_token = jwt.encode(
        {"username":username, "user_id":str(user_id), "role":role, "exp":expires},
        SECRET_KEY, ALGORITHM
    )
    return encoded_access_token

async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        username = payload.get("username")
        role = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTORIZED, detail="Impossível validar usuário.")
        user_model = db.query(User).filter(User.id == user_id).first()
        if user_model is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTORIZED,
                                detail="Usuério não encontrado.")
    
        return {"user_id": user_id, "username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTORIZED, detail="Impossível validar usuário.")


@router.get("/")
async def get_user(current_user: Annotated[dict, Depends(get_current_user)]):
    return {"user": current_user}


@router.post("/token", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def login_for_access_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user = await authenticate_user(form.username, form.password, db)
    if not user: raise HTTPException(status_code=status.HTTP_401_UNAUTORIZED, detail="Impossível validar usuário.")

    token = await create_access_token(user.id, user.username, user.role, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    db: Annotated[Session, Depends(get_db)],
    create_user_request: CreateUserRequest,
):
    user_model = User(
        username=create_user_request.username,
        email=create_user_request.email,
        hashed_password=hash_password(create_user_request.password),
        role=create_user_request.role
    )

    db.add(user_model)
    db.commit()