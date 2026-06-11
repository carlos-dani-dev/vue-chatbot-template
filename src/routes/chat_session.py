from starlette import status
from typing import Annotated
from pydantic import BaseModel, EmailStr
from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request

from jose import JWTError, jwt
from ..config import SECRET_KEY, ALGORITHM

from sqlalchemy.orm import Session
from ..database import SessionLocal

from ..schemas.auth import TokenResponse, CreateUserRequest
from ..schemas.chat_session import ChatSessionResponse, CreateChatSessionRequest, ChatSessionListResponse
from ..models import User, ChatSession

from .auth import get_current_user

router = APIRouter(
    prefix="/chats",
    tags=["chats"]
)


def get_db():
    """
    Abre uma nova conexão com o banco de dados e a retorna (yield)
    Após o fim do escopo em que a função get_db é chamada, a conexão é fechada
    """

    db = SessionLocal()
    try: yield db
    finally: db.close()


@router.get("", response_model=ChatSessionListResponse, status_code=status.HTTP_200_OK)
async def list_user_chat_sessions(
    user: Annotated[TokenResponse, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    
    chat_sessions = db.query(ChatSession).filter(ChatSession.user_id == user["user_id"]).all()
    if chat_sessions is None or chat_sessions is []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário sem chats criados.")

    user_sessions_list = []
    for cs in chat_sessions:
        chat_session_response = ChatSessionResponse(
            id=cs.id,
            user_id=cs.user_id,
            title=cs.title,
            created_at=cs.created_at,
            session_metadata=cs.session_metadata
        )
        user_sessions_list.append(chat_session_response)
    
    return ChatSessionListResponse(items=user_sessions_list)


@router.get("/{chat_session_id}", response_model=ChatSessionResponse, status_code=status.HTTP_200_OK)
async def get_user_chat_session(
    chat_session_id: str,
    user: Annotated[TokenResponse, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):

    chat_session = db.query(ChatSession).filter(ChatSession.id == chat_session_id).first()
    if chat_session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat não encontrado.")
    
    chat_session_response = ChatSessionResponse(
        id=chat_session.id,
        user_id=chat_session.user_id,
        title=chat_session.title,
        created_at=chat_session.created_at,
        session_metadata=chat_session.session_metadata
    )

    return chat_session_response


@router.post("/", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_chat_session(
    payload: CreateChatSessionRequest,
    user: Annotated[TokenResponse, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    
    chat_session_model = ChatSession(user_id=user["user_id"], title=payload.title, session_metadata=payload.session_metadata)
    db.add(chat_session_model)
    db.commit()

    chat_session_response = ChatSessionResponse(user_id=user["user_id"], title=chat_session_model.title, session_metadata=chat_session_model.session_metadata)
    return chat_session_response


@router.delete("/{chat_session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_session(
    chat_session_id: str,
    user: Annotated[TokenResponse, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):

    chat_session = db.query(ChatSession).filter(ChatSession.id == chat_session_id).first()
    if chat_session is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat não encontrado.")

    db.query(ChatSession).filter(ChatSession.id == chat_session_id).delete()
    db.commit()