from fastapi import FastAPI, Depends
from database import engine, SessionLocal
from models import Base, Todo
from schemas import TodoCreate
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "hlo world"}

@app.post("/todos")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = Todo(title=todo.title)

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return {
        "message": "Todo Created",
        "data": {
            "id": new_todo.id,
            "title": new_todo.title
        }
    }

@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return todos

@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        return {"message": "Todo not found"}
    
    db.delete(todo)
    db.commit()

    return {"message": "Todo Deleted"}

@app.put("/todo/{todo_id}")
def update_todo(todo_id: int, update_todo: TodoCreate, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        return {"message": "Todo not found"}
    
    todo.title = update_todo.title
    db.commit()
    db.refresh(todo)

    return {
        "message": "Todo updated",
        "data": todo
    }