from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from db.data import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key= True, index= True)
    username : Mapped[str] = mapped_column(String(50), unique= True)
    role : Mapped[str] = mapped_column(String(10),default= "Customer")
    email : Mapped[str] = mapped_column(String(50),unique=True)
    password: Mapped[str] = mapped_column(String(250))
    