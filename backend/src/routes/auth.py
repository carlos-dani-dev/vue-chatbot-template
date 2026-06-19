from starlette import status
from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm



from sqlalchemy.orm import Session
from ..database import SessionLocal

from ..schemas.user_schema import CreateUserRequest, CreateUserResponse, TokenResponse

from ..services.user_service import UserService, get_current_user, hash_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()


def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:
    return UserService(db)


@router.get("/")
async def get_user(current_user: Annotated[dict, Depends(get_current_user)]):
    return {"user": current_user}


@router.post("/token", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def login_for_access_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service_dependency: Annotated[UserService, Depends(get_user_service)]
):
    user = await user_service_dependency.authenticate_user(form.username, form.password)
    if not user: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Impossível validar usuário.")

    token = await user_service_dependency.create_access_token(user.id, user.username, user.role, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: CreateUserRequest,
    user_service_dependency: Annotated[UserService, Depends(get_user_service)]
) -> CreateUserResponse:
    user_model = await user_service_dependency.create_user(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role
    )

    return CreateUserResponse(email=user_model.email, username=user_model.username, role=user_model.role)