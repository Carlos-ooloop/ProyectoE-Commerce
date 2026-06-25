from pydantic import BaseModel
from typing import Optional, Any


class CategoryCreate(BaseModel):
    name:str
    parent_id: Optional[int] = None
     
class CategoryResponse(BaseModel):
    name:str
    parent_id : Optional[int] = None   
     
class CategoryUpdate(BaseModel):
    name : Optional[str] = None
    parent_id : Optional[int] = None    
    
    