from sqlalchemy import Column, Integer,String,Boolean,DateTime,JSON,Float,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.data import Base
from datetime import datetime



class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, index= True, primary_key=True)
    name : Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    parent_id : Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=True)
    products = relationship("Product", back_populates="category")