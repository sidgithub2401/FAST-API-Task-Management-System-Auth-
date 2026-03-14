from pydantic import BaseModel , Field
from typing import Annotated , List 


class TaskSchema(BaseModel):
    title: Annotated[str, Field(..., example="Complete the project documentation")]
    description: Annotated[str, Field(..., example="Write detailed documentation for the project")]
    is_completed: Annotated[bool, Field(..., example=False)]


class TaskResponseSchema(BaseModel):
    id :int
    title: str
    description: str
    is_completed: bool
    user_id: int
