from sqlalchemy import Column, String, Boolean, JSON, ForeignKey, DateTime,Integer,Float,Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column
from db.data import Base
from app.enums.payment_status import PaymentStatus

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column (Integer, primary_key=True)
    order_id : Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"))
    amount: Mapped[float] = mapped_column(Float)
    status = Column(SqlEnum(PaymentStatus), nullable=False,default=PaymentStatus.PENDING)
    provider : Mapped[str] = mapped_column(String(50))
    created_at = Column(DateTime)