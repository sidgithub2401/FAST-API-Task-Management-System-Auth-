from sqlalchemy.orm import Session 
from src.tasks.dtos import TaskSchema 
from src.tasks.model import TaskModel 
from src.users.model import UserModel
from fastapi import HTTPException


def get_all_tasks(db:Session , user: UserModel):
    task = db.query(TaskModel).filter(TaskModel.user_id == user.id).all()
    return task

def create_task(body:TaskSchema , db:Session , user: UserModel):
    task = db.query(TaskModel).filter(TaskModel.title == body.title).first()
    if task:
        raise HTTPException(status_code = 400 , detail = "The Task is already present")
    else:
        new_task = TaskModel(title = body.title , description = body.description , is_completed = body.is_completed , user_id = user.id)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    
def update_task(id:int , body : TaskSchema , db:Session , user:UserModel):
    task = db.query(TaskModel).filter(TaskModel.user_id == user.id , TaskModel.id == id).first()
    if not task:
        raise HTTPException(status_code = 404 , detail = "The task does not belong to you ")
    task.title = body.title
    task.description = body.description
    task.is_completed = body.is_completed
    db.commit()
    db.refresh(task)
    return task


def delete_task(id:int , db:Session , user:UserModel):
    task = db.query(TaskModel).filter(TaskModel.user_id == user.id , TaskModel.id == id).first()
    if not task:
        raise HTTPException(status_code = 404 , detail = "The task does not belong to you ")
    db.delete(task)
    db.commit()
    return {"message" : "Task deleted successfully"}
