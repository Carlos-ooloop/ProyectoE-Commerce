from pydantic import BaseModel
from typing import Any, Optional

class InventoryAdjust(BaseModel):
    quantity : int
    