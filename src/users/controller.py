from src.users.dtos import UserSchema , UserSchemaOut , LoginSchema , DeleteUserSchema
from src.users.model import UserModel
from sqlalchemy.orm import Session 
from fastapi import HTTPException
from pwdlib import PasswordHash
import jwt
from dotenv import load_dotenv
import os 
from datetime import  datetime , timedelta , timezone

load_dotenv()

secret_key = os.getenv("SECRET_KEY")    
secret_algorithm = os.getenv("ALGORITHM")
expire = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS"))

password_hash = PasswordHash.recommended()


def getusers(db:Session):
    users = db.query(UserModel).all()
    return users 


def create_user(body:UserSchema , db:Session):
    user = db.query(UserModel).filter(UserModel.email ==body.email).first()
    if user :
        raise HTTPException (status_code=400 , detail="User with this email already exists")
    else:
        password = password_hash.hash(body.password)
        new_user = UserModel(name = body.name , username = body.username , email = body.email , hashed_password = password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
def login_user(body:LoginSchema , db:Session):
    user = db.query(UserModel).filter(UserModel.email ==body.email).first()
    if not user:
        raise HTTPException(status_code=404 , detail="User not found")
    else:
        if password_hash.verify(body.password , user.hashed_password):

            time_expire = datetime.now(timezone.utc) + timedelta(minutes=expire)

            token_payload = {"user_id": user.id, "email": user.email , "exp": time_expire}

            token = jwt.encode(payload=token_payload, algorithm=secret_algorithm, key=secret_key)

            return {"message": "Login successful", "token": token , "token_type": "bearer"} 
        else:
            raise HTTPException(status_code=401 , detail="Invalid credentials")
        
def update_user(body:UserSchema , user : UserModel ,db:Session) :
        if body.email == user.email:
            user_present = db.query(UserModel).filter(UserModel.email == body.email).first()
            if user_present:
                user_present.name = body.name
                user_present.username = body.username
                user_present.email = body.email
                user_present.hashed_password = password_hash.hash(body.password)
            db.commit()
            db.refresh(user_present)
            return user_present
        else:
            raise HTTPException(status_code=401 , detail="You are not Authorized to updated the details")
        
def delete_user(body: DeleteUserSchema , user : UserModel, db:Session):
    if user.email == body.email:
        user_present = db.query(UserModel).filter(UserModel.email == body.email).first()
        if user_present:
            db.delete(user_present)
            db.commit()
            return {"message": "User deleted successfully"}
        else:
            raise HTTPException(status_code=404 , detail="User not found")
    else:
        raise HTTPException(status_code=401 , detail="You are not Authorized to delete the user")

