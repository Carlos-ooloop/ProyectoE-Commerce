from pydantic import BaseModel
from typing import Any, Optional

class OrderItemCreate(BaseModel):
    product_id : int
    quantity:int
    
    
    
class OrderCreate(BaseModel):
    items : list[OrderItemCreate]    