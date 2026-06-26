from pydantic import BaseModel
from typing import Optional, Any


class PaymentCreate(BaseModel):
    order_id : int
    client_money: float