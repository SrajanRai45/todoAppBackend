from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request
from sqlalchemy.orm import Session

from database.database import get_db
from models.models import Todos

router = APIRouter()


@router.get("/allTasks")
async def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(Todos).all()

@router.get
