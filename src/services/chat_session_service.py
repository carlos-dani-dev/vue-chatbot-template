import uuid
import time

from dataclasses import dataclass, field
from typing import TypedDict, Literal, Protocol, Any

from ..config import CHAT_DEFAULT_SYSTEM_PROMPT

from ..models import ChatSession, User
from ..schemas.openaiLike_schema import ChatCompletionRequest, ChatCompletionMetadata, ChatMessage
from ..repository.chat_session_repository import ChatSessionRepository


@dataclass
class ChatResult:
    response: dict[str, Any]
    metadata: ChatCompletionMetadata


class ContextMessage(TypedDict):
    role: Literal["system", "user", "assistant", "tool"]
    content: str


@dataclass
class ContextResult:
    messages: list[ContextMessage]
    window_size: int
    includes_system: bool = False
    updated_summary: str | None = field(default=None)


class ContextStrategy(Protocol):
    def build(
        self,
        messages: list[ContextMessage],
        *,
        system_prompt: str = "",
        conversation_summary: str | None = None,
    ) -> ContextResult: ...


class ChatSessionService:

    def __init__(self, db, inference_gw, ctxt_strategy = None):
        self.db = db
        self.inference_gw = inference_gw
        self.repo = ChatSessionRepository(db)
        self.ctxt_strategy = ctxt_strategy
        #self.ctxt_strategy_name = 
    

    def resolve_session(self, user_id, session_id, channel) -> ChatSession:
        if session_id:
            existing = self.repo.get_session_by_user_id(session_id, user_id)
            return existing
            #raise ChatNotFoundError(session_id)
        
        public_id = str(uuid.uuid4)
        return self.repo.create_session(
            session_id=public_id,
            user_id=user_id
        )

    @staticmethod
    def resolve_system_prompt(request: ChatCompletionRequest) -> str:
        for message in reversed(request.messages):
            if message.role == "system" and message.content.strip():
                return message.content
        return CHAT_DEFAULT_SYSTEM_PROMPT


    def build_context(self, chat_session: ChatSession, system_prompt: str) -> tuple[list[ChatMessage], int, bool]:
        rows = self.repo.list_messages_by_session_id(chat_session.id)

        history: list[ContextMessage] = [{"role": message.role, "content": message.content} for message in rows]

        result = self.ctxt_strategy.build(
            history,
            system_prompt=system_prompt,
            conversation_summary=chat_session.conversation_summary,
        )

        if result.updated_summary is not None:
            self.repo.update_conversation_summary(chat_session.id, result.updated_summary)
            chat_session.conversation_summary = result.updated_summary
        
        chat_messages = [
            ChatMessage(role=message["role"], content=message["content"]) for message in result.messages
        ]

        return chat_messages, result.window_size, result.includes_system
    
    @staticmethod
    def extract_latest_user(messages: list[ChatMessage]) -> ChatMessage | None:
        for message in reversed(messages):
            if message.role == "user" and message.content:
                return message
        return None


    def build_prompt(self, request:ChatCompletionRequest,
                     context_messages: list[ChatMessage], includes_system: bool) -> list[ChatMessage]:
        
        system_from_request = [message for message in request.messages if message.role == "system"]
        latest_user = self.extract_latest_user(request.messages)

        merged: list[ChatMessage] = []
        if not includes_system:
            if system_from_request:
                merged.extend(system_from_request)
            elif CHAT_DEFAULT_SYSTEM_PROMPT.strip():
                merged.append(ChatMessage(role="system", content=CHAT_DEFAULT_SYSTEM_PROMPT))
        
        merged.extend(context_messages)

        other_roles = [
            message for message in request.messages if message.role not in ("system", "user") and message is not latest_user
        ]

        merged.extend(other_roles)
        if latest_user is not None: merged.append(latest_user)

        return merged

    @staticmethod
    def extract_latest_user(messages: list[ChatMessage]) -> ChatMessage | None:
        for message in reversed(messages):
            if message.role == "user" and message.content:
                return message.content
        return ""

    @staticmethod
    def extract_assistant_content(llm_response: dict[str, Any]):
        choices= llm_response.get("choices")
        if not isinstance(choices, list) or not choices:
            return ""
        first = choices[0]
        if not isinstance(first, dict):
            return ""
        message = first.get("message")
        if not isinstance(message, dict):
            return ""
        content = message.get("content")
        return content if isinstance(content, str) else ""


    def handle(self, request: ChatCompletionRequest, user) -> ChatResult:
        started = time.perf_counter()

        chat_session = self.resolve_session(
            user_id=user.id,
            session_id=request.session_id,
            channel=request.channel    
        )

        system_prompt =  self.resolve_system_prompt(request)

        context_messages, context_size, includes_system = self.build_context(
            chat_session = chat_session,
            system_prompt = system_prompt
        )

        built_messages = self.build_prompt(
            request,
            context_messages,
            includes_system=includes_system
        )

        latest_user = self.latest_user_content(request.messages)
        
        inference_request = request.model_copy(update={"messages": built_messages})
        llm_response = self.inference_gw.chat_completion(inference_request)

        assistant_content = self.extract_assistant_content(llm_response)

        if latest_user:
            self.repo.add_message(
                session_id=chat_session.id,
                role="user",
                content=latest_user
            )
        if assistant_content:
            self.repo.add_message(
                session_id=chat_session.id,
                role="assistant",
                content=assistant_content
            )
        self.db.commit()

        latency_ms = int((time.perf_counter() - started) * 1000)
        metadata = ChatCompletionMetadata(
            session_id=chat_session.id,
            channel=chat_session.channel,
            latency_ms=latency_ms,
            context_windows_size=context_size,
            context_strategy=self.ctxt_strategy_name,
            persisted=True
        )

        response_body = {**llm_response, "metadata": metadata.model_dump()}
        return ChatResult(response=response_body, metadata=metadata)


    ### métodos do endpoint

    def list_chat_sessions_by_user(self, user_id) -> list[ChatSession]:
        return self.repo.list_chat_sessions_by_user_id(user_id)
    
    def get_chat_session(self, chat_session_id, user_id) -> ChatSession:
        return self.repo.get_chat_session_by_id(chat_session_id, user_id)
    
    def create_chat_session(self, chat_id: str | None, user_id, title: str, channel: str):
        if chat_id:
            chat_session = self.repo.get_chat_session_by_id(chat_id, user_id)
            if chat_session is not None:
                return chat_session
        return self.repo.create_chat_session(chat_id, user_id, title, channel)