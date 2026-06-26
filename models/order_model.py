from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.data import Base
from sqlalchemy import Column, Integer, String,Boolean,JSON, DateTime, Float,ForeignKey
from datetime import datetime



class Order(Base):
    
    __tablename__ = "orders"
    id  =  mapped_column(Integer,primary_key=True)
    created_at = mapped_column(DateTime)
    status = mapped_column(String, default="PENDING_PAYMENT")
    total_amount = mapped_column(Float)
    user_id = mapped_column (Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")