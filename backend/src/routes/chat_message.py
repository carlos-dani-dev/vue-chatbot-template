from starlette import status
from typing import Annotated, Dict
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from ..database import SessionLocal

from ..schemas.user_schema import TokenResponse
from ..schemas.chat_message_schema import MessageListResponse, ChatMessage, SendChatMessageResponse, SendChatMessageRequest
from ..models import ChatSession, User
from ..services.chat_session_service import ChatSessionService
from ..services.user_service import UserService
from ..schemas.openaiLike_schema import ChatCompletionRequest, ChatMessageOpenAI

from ..clients.inference_gw import InferenceGateway
from ..clients.inference_client import InferenceHttpClient

from ..exceptions.exceptions import ChatSessionNotFoundError

from .auth import get_current_user

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

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


def serialize_chat_message(message) -> dict:
    return {
        "chat_session_id": message.session_id,
        "role": message.role,
        "content": message.content,
        "created_at": message.created_at,
    }


@router.get("/{chat_id}/messages", response_model=MessageListResponse)
async def list_chat_session_messages(
    chat_id: str,
    user: Annotated[Dict, Depends(get_current_user)],
    chat_service_dependency: Annotated[ChatSessionService, Depends(get_chat_service)] 
):
    try:
        chat_session, list_messages = chat_service_dependency.list_messages(chat_id, user["user_id"])
    except ChatSessionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat não encontrado.") from exc

    return MessageListResponse(
        chat_session_id=chat_session.id,
        list_messages=[ChatMessage.model_validate(serialize_chat_message(message)) 
                       for message in list_messages]
    )


@router.post("/{chat_id}/messages", response_model=SendChatMessageResponse)
async def send_message(chat_id: str, payload: SendChatMessageRequest,
    user: Annotated[Dict, Depends(get_current_user)],
    chat_service_dependency: Annotated[ChatSessionService, Depends(get_chat_service)] 
) -> SendChatMessageResponse:
    try:
        chat_session = chat_service_dependency.get_chat_session(chat_id, user["user_id"])
    except ChatSessionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat não encontrado.") from exc
    
    messages: list[ChatMessageOpenAI] = []
    if payload.system_prompt:
        messages.append(ChatMessageOpenAI(role="system", content=payload.system_prompt))
    messages.append(ChatMessageOpenAI(role="user", content=payload.content))
    
    print(messages)

    request = ChatCompletionRequest(
        model=payload.model,
        messages=messages,
        session_id=chat_id,
        channel=chat_session.channel,
        stream=False
    )

    try:
        result=chat_service_dependency.handle(request, user)
    except Exception as exc:
        raise Exception from exc

    user_row, assistant_row = chat_service_dependency.get_last_interaction(chat_session.id, user["user_id"])
    if user_row is None or assistant_row is None:
        raise HTTPException(status_code=500, detail="As mensagens deste chat não forma persistidas.")

    print(user_row)
    print(assistant_row)

    return SendChatMessageResponse(
        chat_session_id=chat_id,
        user_message=ChatMessage.model_validate(serialize_chat_message(user_row)),
        assistant_message=ChatMessage.model_validate(serialize_chat_message(assistant_row)),
        latency_ms=result.metadata.latency_ms,
        context_window_size=result.metadata.context_window_size,
        ctxt_strategy=result.metadata.context_strategy
    )