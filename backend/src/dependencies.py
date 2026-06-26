from starlette import status
from sqlalchemy.orm import Session

from typing import Annotated

from jose import JWTError, jwt

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from .config import SECRET_KEY, ALGORITHM

# needed db configurations
from .database import SessionLocal

# needed models
from .models import User

# needed services
from .services.chat_service import ChatService
from .services.user_service import UserService

# needed repos
from .repository.user_repository import UserRepository;

from .clients.inference_gw import InferenceGateway
from .clients.inference_client import InferenceHttpClient



oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()


def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        email = payload.get("email")
        role = payload.get("role")

        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Impossível validar usuário.")

        if payload.get("type") == "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido para essa operação")

        user_model = UserRepository(db).get_user_by_id(user_id)
        if user_model is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado.")

        return {"user_id": user_id, "email": email, "role": role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Impossível validar usuário.")


def get_inference_gateway() -> InferenceGateway:
    return InferenceGateway(InferenceHttpClient())


def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:
    return UserService(db)


def get_chat_service(
    db: Session = Depends(get_db),
    gateway: InferenceGateway = Depends(get_inference_gateway),
) -> ChatService:
    return ChatService(db, gateway)


ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
CurrentUserDep: Annotated[User, Depends(get_current_user)]
UserServiceDep: Annotated[UserService, Depends(get_user_service)]