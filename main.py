from fastapi import FastAPI
from src.users.router import user_router
from src.users.model import UserModel                                ##For creating the table in the database 
from src.utils.database import Base , engine
from src.tasks.model import TaskModel 
from src.tasks.router import task_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(task_router)


