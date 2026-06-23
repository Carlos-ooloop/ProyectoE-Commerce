from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    username : str
    role : str
    email : str