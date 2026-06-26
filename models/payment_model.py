from sqlalchemy import Column, String, Boolean, JSON, ForeignKey, DateTime,Integer,Float
from sqlalchemy.orm import Mapped, mapped_column
from db.data import Base

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column (Integer, primary_key=True)
    order_id : Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"))
    amount: Mapped[float] = mapped_column(Float)
    status: Mapped[str]=mapped_column(String)
    provider : Mapped[str] = mapped_column(String)
    created_at = Column(DateTime)