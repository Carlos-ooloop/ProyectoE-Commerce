from pydantic import BaseModel
from typing import Optional
class UserResponse(BaseModel):
    id: int
    username : str
    role : str
    email : str
    
class UserCreate(BaseModel):
    username: str
    email:str
    password:str    
    
class UserUpdate(BaseModel):
    username: Optional[str] = None    
    email : Optional[str] = None
    password : Optional[str] = None