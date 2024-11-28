from app.connections.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.constant.enums.raw_material_types import RawMaterialTypeEnums

class RawMaterials(Base):
    __tablename__ = "raw_materials"
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(Enum(RawMaterialTypeEnums), nullable=False)   
    brand = Column(String(255), nullable=False)
    purchase_unit = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=False)
    quantity_unit = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now(timezone.utc), nullable=True)
    is_deleted = Column(DateTime, default=None, nullable=True)
    
    # # RELATIONSHIPS
    # # relationship to stock_inventory
    # stock = relationship("StockInventory", back_populates="raw_materials", uselist=False)
    
    # # relationship to menu_ingredients
    # menu_ingredient = relationship("MenuIngredients", back_populates="raw_materials")
    
    # # relationship to PO
    # purchase_order = relationship("PurchaseOrder", back_populates="raw_materials")
    
    # # relationship to PR
    # purchase_request = relationship("PurchaseRequest", back_populates="raw_materials")
    
    # # relationship to market_lists
    # market_list = relationship("MarketList", back_populates="raw_materials", uselist=False)
    
    def to_dict(self):
        raw_materials = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "brand": self.brand,
            "purchase_unit": self.purchase_unit,
            "quantity": self.quantity,
            "quantity_unit": self.quantity_unit,
            "metadata": {
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "is_deleted": self.is_deleted
            }
        }
        
        return raw_materials