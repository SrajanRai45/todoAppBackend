from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Request, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_CONTENT

from database.database import get_db
from models.models import Todos
from models.validation import TodoRequest

routerV1 = APIRouter()


@routerV1.get("/allTodos", status_code=HTTP_200_OK)
async def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(Todos).all()


@routerV1.get("/todo/{todo_id}", status_code=HTTP_200_OK)
async def read_todo(db: Annotated[Session, Depends(get_db)], todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@routerV1.post("/todo", status_code=status.HTTP_201_CREATED)
async def createTodo(
    db: Annotated[Session, Depends(get_db)], todo_request: TodoRequest
):
    todo_model = Todos(**todo_request.dict())
    db.add(todo_model)
    db.commit()


@routerV1.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def updateTodo(
    db: Annotated[Session, Depends(get_db)],
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="todo not found")

    todo_model.title = todo_request.title
    todo_model.complete = todo_request.complete
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority

    db.add(todo_model)
    db.commit()


@routerV1.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteTodo(
    db: Annotated[Session, Depends(get_db)], todo_id: int = Path(get=0)
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=422, detail="Todo not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()
