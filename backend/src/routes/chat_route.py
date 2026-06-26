from typing import Annotated
from starlette import status
from fastapi import Depends, APIRouter, HTTPException

# needed schemas
from ..schemas.chat_session_schema import ChatSessionResponse, ChatSessionListResponse # response schemas
from ..schemas.chat_session_schema import CreateChatSessionRequest # request schemas

# needed models
from ..models import User

# needed services
from ..services.chat_service import ChatService

# needed dependencies
from ..dependencies import get_chat_service, get_current_user, get_inference_gateway

from ..clients.inference_gw import InferenceGateway
from ..clients.inference_client import InferenceHttpClient


router = APIRouter(
    prefix="/chats",
    tags=["chats"]
)


@router.get("", response_model=ChatSessionListResponse, status_code=status.HTTP_200_OK)
async def list_user_chat_sessions(CurrentUserDep: Annotated[User, Depends(get_current_user)], ChatServiceDep: Annotated[ChatService, Depends(get_chat_service)]):
    
    chat_sessions = ChatServiceDep.list_chat_sessions_by_user(CurrentUserDep["user_id"])
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
async def get_user_chat_session(CurrentUserDep: Annotated[User, Depends(get_current_user)], ChatServiceDep: Annotated[ChatService, Depends(get_chat_service)], chat_session_id: str):

    chat_session = ChatServiceDep.get_chat_session(chat_session_id, CurrentUserDep["user_id"])
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
    CurrentUserDep: Annotated[User, Depends(get_current_user)], ChatServiceDep: Annotated[ChatService, Depends(get_chat_service)], payload: CreateChatSessionRequest):
    chat_session_model = ChatServiceDep.create_chat_session(
        None,
        CurrentUserDep["user_id"],
        payload.title,
        payload.channel
    )

    return ChatSessionResponse(id=chat_session_model.id,
                               user_id=chat_session_model.user_id,
                               title=chat_session_model.title,
                               created_at=chat_session_model.created_at,
                               channel=chat_session_model.channel,
                               session_metadata=chat_session_model.session_metadata)


@router.delete("/{chat_session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_session(CurrentUserDep: Annotated[User, Depends(get_current_user)], ChatServiceDep: Annotated[ChatService, Depends(get_chat_service)], chat_session_id: str):

    return ChatServiceDep.delete_chat_session(chat_session_id, CurrentUserDep["user_id"])
