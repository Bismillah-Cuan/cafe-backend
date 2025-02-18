from app.connections.db import Base
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Boolean, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class MarketList(Base):
    __tablename__ = "market_list"
    
    id = Column(Integer, primary_key=True, nullable=False)
    product_name = Column(String(255), nullable=False)
    product_price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now(timezone.utc), nullable=True) 
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "product_name": self.product_name,
            "product_price": self.product_price,
            "quantity": self.quantity,
            "metadata": {
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "is_deleted": self.is_deleted
            }
        }