from starlette import status
from typing import Annotated, Dict
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from ..database import SessionLocal

from ..schemas.user_schema import TokenResponse
from ..schemas.chat_session_schema import ChatSessionResponse, CreateChatSessionRequest, ChatSessionListResponse
from ..models import ChatSession, User
from ..services.chat_session_service import ChatSessionService
from ..services.user_service import UserService

from ..clients.inference_gw import InferenceGateway
from ..clients.inference_client import InferenceHttpClient

from ..services.user_service import get_current_user

router = APIRouter(
    prefix="/chats",
    tags=["chats"]
)


def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_inference_gateway() -> InferenceGateway:
    return InferenceGateway(InferenceHttpClient())

def get_chat_service(
    db: Session = Depends(get_db),
    gateway: InferenceGateway = Depends(get_inference_gateway),
) -> ChatSessionService:
    return ChatSessionService(db, gateway)


@router.get("", response_model=ChatSessionListResponse, status_code=status.HTTP_200_OK)
async def list_user_chat_sessions(
    user: Annotated[Dict, Depends(get_current_user)],
    chat_service_dependency: Annotated[ChatSessionService, Depends(get_chat_service)]
):
    
    chat_sessions = chat_service_dependency.list_chat_sessions_by_user(user["user_id"])
    if chat_sessions is None or chat_sessions is []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário sem chats criados.")

    user_sessions_list = []
    for cs in chat_sessions:
        chat_session_response = ChatSessionResponse(
            id=cs.id,
            user_id=cs.user_id,
            title=cs.title,
            created_at=cs.created_at,
            channel=cs.channel,
            session_metadata=cs.session_metadata
        )
        user_sessions_list.append(chat_session_response)
    
    return ChatSessionListResponse(items=user_sessions_list)


@router.get("/{chat_session_id}", response_model=ChatSessionResponse, status_code=status.HTTP_200_OK)
async def get_user_chat_session(
    user: Annotated[Dict, Depends(get_current_user)],
    chat_session_id: str,
    chat_service_dependency: Annotated[ChatSessionService, Depends(get_chat_service)]
):

    chat_session = chat_service_dependency.get_chat_session(chat_session_id, user["user_id"])
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
    user: Annotated[Dict, Depends(get_current_user)],
    payload: CreateChatSessionRequest,
    chat_service_dependency: Annotated[ChatSessionService, Depends(get_chat_service)]
):
    chat_session_model = chat_service_dependency.create_chat_session(
        None,
        user["user_id"],
        "Título do Chat_Session",
        payload.channel
    )

    chat_service_dependency.db.add(chat_session_model)
    chat_service_dependency.db.commit()

    return ChatSessionResponse(id=chat_session_model.id,
                               user_id=chat_session_model.user_id,
                               title=chat_session_model.title,
                               created_at=chat_session_model.created_at,
                               channel=chat_session_model.channel,
                               session_metadata=chat_session_model.session_metadata)


@router.delete("/{chat_session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_session(
    chat_session_id: str,
    user: Annotated[Dict, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):

    chat_session = db.query(ChatSession).filter(ChatSession.id == chat_session_id).first()
    if chat_session is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat não encontrado.")

    db.query(ChatSession).filter(ChatSession.id == chat_session_id).delete()
    db.commit()