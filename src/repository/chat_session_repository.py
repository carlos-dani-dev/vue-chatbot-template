import uuid

from ..exceptions.exceptions import ChatSessionNotFoundError

from sqlalchemy import select
from sqlalchemy.orm import Session

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