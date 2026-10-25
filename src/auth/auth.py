from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from models.models import User
from models.validation import CreateUserRequest

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
        hashed_password=create_user_request.password,
        role=create_user_request.role,
    )
    db.add(create_model_user)
    db.commit()


@routerAuth.get("/authAll")
async def get_all_user(db: Annotated[Session, Depends(get_db)]):
    return db.query(User).all()
