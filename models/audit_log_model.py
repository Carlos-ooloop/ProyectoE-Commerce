from sqlalchemy import Column, String, Boolean, JSON, Enum as SqlEnum,Integer,DateTime
from sqlalchemy.orm import Session, relationship, Mapped, mapped_column
from db.data import Base
from datetime import datetime
from app.enums.audit_types import AuditAction,AuditEntity

class AuditLog(Base):
    __tablename__ = "auditlog"
    
    id = Column(Integer, primary_key=True)
    entity_type : Mapped[str] = mapped_column(SqlEnum(AuditEntity))
    entity_id : Mapped[int] = mapped_column(Integer)
    action : Mapped[str] = mapped_column(SqlEnum(AuditAction))
    user_id : Mapped[int] = mapped_column(Integer,nullable=False)
    status_before : Mapped[str] = mapped_column(String(50), nullable=True)
    status_after: Mapped[str]= mapped_column(String(50), nullable=True)
    details = Column(JSON, nullable=True)
    created_at = Column (DateTime, default=datetime.utcnow)