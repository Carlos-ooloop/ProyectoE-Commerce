from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.data import Base
from sqlalchemy import Column, Integer, String,Boolean,JSON, DateTime, Float,ForeignKey, Enum as SqlEnum
from datetime import datetime
from app.enums.order_status import OrderStatus



class Order(Base):
    
    __tablename__ = "orders"
    id  =  mapped_column(Integer,primary_key=True)
    created_at = mapped_column(DateTime,default=datetime.utcnow)
    status = Column(SqlEnum(OrderStatus),nullable=False, default=OrderStatus.PENDING_PAYMENT)
    total_amount = mapped_column(Float)
    user_id = mapped_column (Integer, ForeignKey("users.id"))
    users = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")