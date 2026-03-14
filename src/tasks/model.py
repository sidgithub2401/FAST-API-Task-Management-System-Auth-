from src.utils.database import Base 
from sqlalchemy import Column , Integer , String , ForeignKey , Boolean 

class TaskModel(Base):
    __tablename__ = 'tasks_table'
    id = Column(Integer, primary_key= True , index = True)
    title = Column(String , nullable=False)
    description = Column(String , nullable=False)
    is_completed = Column(Boolean , default=False)
    user_id = Column(Integer , ForeignKey("usertable.id",ondelete = "CASCADE"),)