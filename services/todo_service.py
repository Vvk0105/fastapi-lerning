from models.todo import Todo

def get_all_todos(db):
    return db.query(Todo).all()


def create_new_todo(db, title):
    new_todo = Todo(title=title)

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo


def delete_existing_todo(db, todo_id):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        return None

    db.delete(todo)
    db.commit()

    return todo

def complete_todo(db, todo_id):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        return None
    
    todo.completed = True

    db.commit()
    db.refresh(todo)

    return todo