from sqlalchemy import Column, Integer,String,Boolean,DateTime,JSON,Float,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.data import Base
from datetime import datetime

class Inventory(Base):
    
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key= True, index=True)
    product_id : Mapped[int] = mapped_column(Integer, ForeignKey("products.id"),unique=True,nullable=False)
    quantity : Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,onupdate=datetime.utcnow)
    product = relationship("Product", back_populates="inventory")






