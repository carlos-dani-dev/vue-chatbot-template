from starlette import status
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from ..database import SessionLocal

from ..schemas.auth import TokenResponse
#from ..schemas.chat_message_schema import 
from ..models import ChatSession, ChatMessage

from .auth import get_current_user
