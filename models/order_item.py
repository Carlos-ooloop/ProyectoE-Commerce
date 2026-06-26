from sqlalchemy import Column, Integer,Float,DateTime,String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from db.data import Base
from datetime import datetime

class OrderItem(Base):
    
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True)
    order_id = mapped_column(Integer, ForeignKey("orders.id"))
    product_id = mapped_column(Integer, ForeignKey("products.id"))
    quantity = mapped_column(Integer)
    unit_price = mapped_column(Float)
