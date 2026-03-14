from src.utils.database import Base
from sqlalchemy import Column , Integer , String

class UserModel(Base):
    __tablename__ = "usertable"
    id = Column(Integer , primary_key= True , index= True)
    name = Column(String)
    username = Column(String)
    email = Column(String , nullable = False , unique= True)
    hashed_password = Column(String , nullable= False)