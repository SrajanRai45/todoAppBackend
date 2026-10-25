from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.models.models import User
from src.models.validation import CreateUserRequest

# pre-requisit functions
passwordHash = PasswordHash((Argon2Hasher(),))


def getPasswordHash(password: str) -> str:
    return passwordHash.hash(password)


def authenticateUser(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not passwordHash.verify(password, user.hashed_password):
        return False
    return True


routerAuth = APIRouter()


@routerAuth.post("/auth/")
async def get_user(
    db: Annotated[Session, Depends(get_db)], create_user_request: CreateUserRequest
):
    create_model_user = User(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=getPasswordHash(create_user_request.password),
        role=create_user_request.role,
    )
    db.add(create_model_user)
    db.commit()


@routerAuth.get("/authAll")
async def get_all_user(db: Annotated[Session, Depends(get_db)]):
    return db.query(User).all()


@routerAuth.post("/token")
async def login_for_access_token(
    from_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user = authenticateUser(from_data.username, from_data.password, db)
    if not user:
        return {"failure"}
    return {"success"}
