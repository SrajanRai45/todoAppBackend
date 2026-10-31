from datetime import datetime, timedelta, timezone
import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, oauth2
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from src.database.database import get_db
from src.models.models import User
from src.models.validation import CreateUserRequest, Token

# pre-requisit functions
passwordHash = PasswordHash((Argon2Hasher(),))
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def getPasswordHash(password: str) -> str:
    return passwordHash.hash(password)


def authenticateUser(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not passwordHash.verify(password, user.hashed_password):
        return False
    return user


routerAuth = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "b728e08d8cbedc7b4976ca620b66c6ea37f5d3aabeb555dffd05ea2bb1f6d213"
ALGORITHM = "HS256"


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Couldn't validate user",
            )
        return {"username": username, "user_id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate user"
        )


@routerAuth.post(
    "/CreateUser/", description="create a user", status_code=status.HTTP_201_CREATED
)
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


@routerAuth.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user = authenticateUser(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate user"
        )

    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}
