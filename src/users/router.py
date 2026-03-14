from fastapi import APIRouter , Depends , status , Request
from src.utils.database import get_db
from src.users.model import UserModel
from src.users.dtos import UserSchema , UserSchemaOut , LoginSchema , DeleteUserSchema
from src.users.controller import create_user , getusers , login_user , update_user , delete_user
from src.utils.helper import authourize_user
from sqlalchemy.orm import Session
from typing import List


user_router = APIRouter(prefix="/users" , tags = ["users"])

db_dependency = Depends(get_db)

@user_router.get("/", response_model=List[UserSchemaOut], status_code= status.HTTP_200_OK)
def getusersall(db:Session = db_dependency):
    return getusers(db)


@user_router.post("/create_user", response_model = UserSchemaOut , status_code=status.HTTP_201_CREATED)
def create_user_new(body: UserSchema , db: Session = db_dependency):
    return create_user(body , db)

@user_router.post("/login", status_code=status.HTTP_200_OK)
def login_user_new(body: LoginSchema , db: Session = db_dependency):
    return login_user(body , db)

@user_router.put("/update_user", response_model=UserSchemaOut, status_code=status.HTTP_200_OK)
def update_user_new(body: UserSchema , user: UserModel = Depends(authourize_user) , db: Session = db_dependency):
    return update_user(body, user, db)

@user_router.delete("/delete_user", status_code=status.HTTP_200_OK)
def delete_user_new(body: DeleteUserSchema , user: UserModel = Depends(authourize_user) , db: Session = db_dependency):
    return delete_user(body, user, db)