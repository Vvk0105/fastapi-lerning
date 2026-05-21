from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from schemas.todo_schema import TodoCreate, TodoResponse
from services.todo_service import (
    get_all_todos,
    create_new_todo,
    delete_existing_todo,
    complete_todo
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/todos", response_model=list[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    return get_all_todos(db)


@router.post("/todos")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    return create_new_todo(db, todo.title)


@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    deleted = delete_existing_todo(db, todo_id)

    if not deleted:
        return {"message": "Todo not found"}

    return {"message": "Todo deleted"}

@router.patch("/todos/{todo_id}/complete")
def mark_completed(todo_id: int, db: Session = Depends(get_db)):
    todo = complete_todo(db, todo_id)

    if not todo:
        return {"message": "Todo not found"}
    
    return todo