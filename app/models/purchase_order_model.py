from app.connections.db import Base
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Boolean, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.constant.enums.po_status import POStatus
from app.constant.enums.divisions import DivisionEnums

class PurchaseOrder(Base):
    __tablename__ = "purchase_order"
    
    id = Column(Integer, primary_key=True, nullable=False)
    po_code = Column(String(255), nullable=False)
    supplier_id = Column(Integer, ForeignKey("supplier.id"), nullable=True)
    purchase_request_id = Column(Integer, ForeignKey("purchase_request.id"), nullable=False)
    raw_material_id = Column(Integer, ForeignKey("raw_materials.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    division = Column(Enum(DivisionEnums), nullable=False)
    received_qty = Column(Float, nullable=False, default=0)
    received_notes = Column(String(255), nullable=True)
    supplier_notes = Column(String(255), nullable=True)
    po_status = Column(Enum(POStatus), nullable=False, default=POStatus.NEW)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now(timezone.utc), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    # Relationship from Supplier
    supplier = relationship("Supplier", foreign_keys=[supplier_id], back_populates="purchase_order")
    
    # Relationship from PurchaseRequest
    purchase_request = relationship("PurchaseRequest", foreign_keys=[purchase_request_id], back_populates="purchase_order")
    
    # Relationship from User
    users = relationship("Users", foreign_keys=[user_id], back_populates="purchase_order")
    
    # Relationship from RawMaterials
    raw_materials = relationship("RawMaterials", foreign_keys=[raw_material_id], back_populates="purchase_order")
    
    def to_dict(self):
        return {
            "id": self.id,
            "po_code": self.po_code,
            "supplier_id": self.supplier_id,
            "purchase_request_id": self.purchase_request_id,
            "user_id": self.user_id,
            "division": self.division,
            "received_qty": self.received_qty,
            "received_notes": self.received_notes,
            "supplier_notes": self.supplier_notes,
            "status": self.po_status,
            "metadata": {
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "is_deleted": self.is_deleted
            }
        }
    
