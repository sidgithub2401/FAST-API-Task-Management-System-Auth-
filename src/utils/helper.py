from fastapi import Request , HTTPException , Depends
from sqlalchemy.orm import Session
from src.users.model import UserModel
import jwt 
from dotenv import load_dotenv
import os 
from src.utils.database import get_db

load_dotenv()
secret_key = os.getenv("SECRET_KEY")
secret_algorithm = os.getenv("ALGORITHM")

def authourize_user(request:Request , db:Session = Depends(get_db)) :
    try:
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[-1]
        data = jwt.decode(token , key = secret_key , algorithms = secret_algorithm) 
        print(data)
        email = data.get("email")
        user = db.query(UserModel).filter(UserModel.email == email).first()
        if not user: 
            raise HTTPException ( status_code=401 , detail="Unauthorized")
        else:
            return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token Expired")