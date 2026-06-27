from sqlalchemy import Column, Integer,String,Boolean,DateTime,JSON,Float,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.data import Base
from datetime import datetime


class Product(Base):
    __tablename__ = "products"
    
    id = mapped_column(Integer,primary_key=True,index=True)
    name : Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description = Column(String(500),nullable=False)
    brand : Mapped[str] = mapped_column(String(100), nullable=True)
    category_id : Mapped[int] = mapped_column(Integer,ForeignKey("categories.id"), nullable=False)
    base_price : Mapped[float] = mapped_column(Float, nullable=False)
    unit : Mapped[str] = mapped_column(String(20),nullable=False)
    characteristics = mapped_column(JSON,nullable=True)
    created_at  = mapped_column(DateTime,default= datetime.utcnow)
    updated_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = mapped_column(DateTime, nullable=True)
    
    category = relationship("Category", back_populates="products")
    inventory = relationship("Inventory", uselist= False, back_populates="product")