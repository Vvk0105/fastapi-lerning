from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models.todo import Base
from routers.todo_router import router as todo_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo_router)


@app.get("/")
def home():
    return {"message": "Structured FastAPI App"}