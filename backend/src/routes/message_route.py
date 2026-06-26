from typing import Annotated
from starlette import status
from fastapi import Depends, APIRouter, HTTPException

# needed schemas
from ..schemas.chat_message_schema import MessageListResponse, SendChatMessageResponse
from ..schemas.chat_message_schema import SendChatMessageRequest
from ..schemas.chat_message_schema import ChatMessage
from ..schemas.openaiLike_schema import ChatCompletionRequest, ChatMessageOpenAI

# needed models
from ..models import User

# needed dependencies
from ..dependencies import get_chat_service, get_current_user, get_inference_gateway

# needed services
from ..services.chat_service import ChatService

from ..clients.inference_gw import InferenceGateway
from ..clients.inference_client import InferenceHttpClient

from ..exceptions.exceptions import ChatSessionNotFoundError


def serialize_chat_message(message) -> dict:
    return {
        "chat_session_id": message.session_id,
        "role": message.role,
        "content": message.content,
        "created_at": message.created_at,
    }


router = APIRouter(
    prefix="/chats",
    tags=["chats"]
)


@router.get("/{chat_id}/messages", response_model=MessageListResponse)
async def list_chat_session_messages(CurrentUserDep: Annotated[User, Depends(get_current_user)],
                                     ChatServiceDep: Annotated[ChatService, Depends(get_chat_service)],
                                     chat_id: str):
    try:
        chat_session, list_messages = ChatServiceDep.list_messages(chat_id, CurrentUserDep["user_id"])
    except ChatSessionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat não encontrado.") from exc

    return MessageListResponse(
        chat_session_id=chat_session.id,
        list_messages=[ChatMessage.model_validate(serialize_chat_message(message)) 
                       for message in list_messages]
    )


@router.post("/{chat_id}/messages", response_model=SendChatMessageResponse)
async def send_message(CurrentUserDep: Annotated[User, Depends(get_current_user)],
                       ChatServiceDep: Annotated[ChatService, Depends(get_chat_service)],
                       chat_id: str,
                       payload: SendChatMessageRequest) -> SendChatMessageResponse:
    try:
        chat_session = ChatServiceDep.get_chat_session(chat_id, CurrentUserDep["user_id"])
    except ChatSessionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat não encontrado.") from exc
    
    messages: list[ChatMessageOpenAI] = []
    if payload.system_prompt:
        messages.append(ChatMessageOpenAI(role="system", content=payload.system_prompt))
    messages.append(ChatMessageOpenAI(role="user", content=payload.content))
    
    request = ChatCompletionRequest(
        model=payload.model,
        messages=messages,
        session_id=chat_id,
        channel=chat_session.channel,
        stream=False
    )

    try:
        result=ChatServiceDep.handle(request, CurrentUserDep)
    except Exception as exc:
        raise Exception from exc

    user_row, assistant_row = ChatServiceDep.get_last_interaction(chat_session.id, CurrentUserDep["user_id"])
    if user_row is None or assistant_row is None:
        raise HTTPException(status_code=500, detail="As mensagens deste chat não forma persistidas.")

    return SendChatMessageResponse(
        chat_session_id=chat_id,
        user_message=ChatMessage.model_validate(serialize_chat_message(user_row)),
        assistant_message=ChatMessage.model_validate(serialize_chat_message(assistant_row)),
        latency_ms=result.metadata.latency_ms,
        context_window_size=result.metadata.context_window_size,
        ctxt_strategy=result.metadata.context_strategy
    )