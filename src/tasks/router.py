from fastapi import APIRouter , Depends , status
from src.tasks.model import TaskModel
from src.tasks.controller import create_task , get_all_tasks , update_task , delete_task
from src.utils.database import get_db
from src.utils.helper import authourize_user
from src.users.model import UserModel
from sqlalchemy.orm import Session
from src.tasks.dtos import TaskSchema , TaskResponseSchema


task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.get("/tasks", status_code=status.HTTP_200_OK)
def get_tasks(user: UserModel =Depends(authourize_user),db:Session = Depends(get_db)):
    return get_all_tasks(db , user)

@task_router.post("/create_tasks", response_model=TaskResponseSchema ,status_code=status.HTTP_201_CREATED)
def create_task_route(body: TaskSchema , user: UserModel = Depends(authourize_user) , db:Session = Depends(get_db)):
    return create_task(body , db , user)

@task_router.put("/update_tasks/{id}", response_model=TaskResponseSchema ,status_code=status.HTTP_200_OK)
def update_task_route(id:int , body: TaskSchema , user: UserModel = Depends(authourize_user) , db:Session = Depends(get_db)):
    return update_task(id , body , db , user)

@task_router.delete("/delete_tasks/{id}" ,status_code=status.HTTP_200_OK)
def delete_task_route(id:int , user: UserModel = Depends(authourize_user) , db:Session = Depends(get_db)):
    return delete_task(id , db , user)