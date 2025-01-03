from app.connections.db import Base
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Supplier(Base):
    __tablename__ = "supplier"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=True)
    phone_number = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now(timezone.utc), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    # Relationship to PurchaseOrder
    # purchase_order = relationship("PurchaseOrder", back_populates="supplier")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "phone_number": self.phone_number,
            "metadata": {
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "is_deleted": self.is_deleted
            }
        }