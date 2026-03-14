from pydantic import BaseModel , Field 
from typing import Annotated , List


class UserSchema(BaseModel):
    name : Annotated[str, Field(description="The name of the user")]
    username : Annotated[str, Field(description="The username of the user")]
    email : Annotated[str, Field(...,description="The email of the user")]
    password : Annotated[str, Field(...,description="The password of the user")]

class UserSchemaOut(BaseModel):
    id : Annotated[int, Field(description="The ID of the user")]
    name : Annotated[str, Field(description="The name of the user")]
    username : Annotated[str, Field(description="The username of the user")]
    email : Annotated[str, Field(...,description="The email of the user")]

class LoginSchema(BaseModel):
    email : Annotated[str, Field(...,description="The email of the user")]
    password : Annotated[str, Field(...,description="The password of the user")]

class DeleteUserSchema(BaseModel):
    email : Annotated[str, Field(...,description="The email of the user to be deleted")]