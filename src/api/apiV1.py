from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Path
from sqlalchemy.orm import Session

from database.database import get_db
from models.models import Todos

routerV1 = APIRouter()


@routerV1.get("/allTodos")
async def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(Todos).all()


@routerV1.get("/todo/{todo_id}")
async def read_todo(db: Annotated[Session, Depends(get_db)], todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")
