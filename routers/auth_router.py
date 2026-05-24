from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from schemas.user_schema import UserCreate, LoginSchema
from auth import (
    hash_password,
    verify_password,
    create_access_token
)
from fastapi import HTTPException

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )
    
    # if existing_user:
    #     return {"message": "email already exists"}
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    hashed_password = hash_password(user.password)

    new_user = User(
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created"}

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    
    db_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if not db_user:
        return {"message": "Invalid email"}
    
    validate_password = verify_password(
        user.password,
        db_user.password
    )

    if not validate_password:
        return {"message": "Invalid password"}
    
    token = create_access_token(
        {"sub": db_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }