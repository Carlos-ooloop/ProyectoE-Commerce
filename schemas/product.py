from typing import Optional, Any
from pydantic import BaseModel

class ProductCreate(BaseModel):
    name : str
    description : Optional[str] = None
    brand : str
    category_id : int
    base_price : float
    unit : str
    characteristics : dict[str,Any] | None = None
    
class ProductResponse(BaseModel):
    id: int
    name : str
    description : Optional[str] = None
    brand : str
    category_id : int
    base_price : float
    unit : str
    characteristics : dict[str,Any] | None = None
    
class ProductUpdate(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None
    brand : Optional[str] = None
    category_id : Optional[int] = None
    base_price : Optional[float] = None
    unit : Optional[str] = None
    characteristics : dict[str,Any] | None = None
        
    