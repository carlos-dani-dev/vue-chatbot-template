import uuid
from datetime import UTC, datetime

from ..exceptions.exceptions import ChatSessionNotFoundError

from ..models import ChatMessage
from ..models import ChatSession


class ChatSessionRepository():
    def __init__(self, db):
        self.db = db
    

    def list_chat_sessions_by_user_id(self, user_id: str):
        return self.db.query(ChatSession).filter((ChatSession.user_id == user_id)).all()

    def get_chat_session_by_id(self, session_id: str | None, user_id: str):
        chat_session = self.db.query(ChatSession).filter((ChatSession.id == session_id)
                                                 and (ChatSession.user_id == user_id)).first()
        return chat_session
    
    def create_chat_session(self, chat_id: str, user_id: str, title: str, channel: str):
        chat_session = ChatSession(id=chat_id, user_id=user_id, title=title, 
                                   channel=channel, session_metadata={"str": "str"})
        self.db.add(chat_session)
        self.db.flush()
        return chat_session

    def list_messages_by_chat_session(self, chat_id: str):
        chat_messages = self.db.query(ChatMessage).filter(ChatMessage.session_id == chat_id).all()
        return chat_messages

    def update_chat_session_summary(self, chat_id: str, update_summary: str):
        chat_session = self.db.query(ChatSession).filter(ChatSession.id == chat_id).first()
        if chat_session is not None:
            chat_session.chat_session_summary = update_summary
            self.db.commit()
    
    def create_chat_message(self, chat_id: str, role: str, content: str) -> ChatMessage:
        chat_message = ChatMessage(session_id=chat_id, role=role, content=content, created_at=  datetime.now(UTC))
        self.db.add(chat_message)
        self.db.flush()
        return chat_message