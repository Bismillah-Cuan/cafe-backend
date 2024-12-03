from app.connections.db import Base
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class StockInventory(Base):
    __tablename__ = "stock_inventory"
    
    id = Column(Integer, primary_key=True, nullable=False)
    raw_material_id = Column(Integer, ForeignKey("raw_materials.id"), nullable=False, unique=True)
    quantity = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now(timezone.utc), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    # relationship from RawMaterials
    raw_materials = relationship("RawMaterials", foreign_keys=[raw_material_id], back_populates="stock")
    
    def to_dict(self):
        return {
            "id": self.id,
            "raw_material_id": self.raw_material_id,
            "quantity": self.quantity,
            "metadata": {
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "is_deleted": self.is_deleted
            }
        }