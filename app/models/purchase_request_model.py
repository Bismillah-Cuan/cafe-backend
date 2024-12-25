from app.connections.db import Base
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Boolean, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.constant.enums.divisions import DivisionEnums
from app.constant.enums.pr_status import PRStatus

class PurchaseRequest(Base):
    __tablename__ = "purchase_request"
    
    id = Column(Integer, primary_key=True, nullable=False)
    pr_code = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    division = Column(Enum(DivisionEnums), nullable=False)
    raw_material_id = Column(Integer, ForeignKey("raw_materials.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    pr_status = Column(Enum(PRStatus), nullable=False, default=PRStatus.REQUESTED)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now(timezone.utc), nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    # Relationship from PurchaseRequest
    raw_materials = relationship("RawMaterials", back_populates="purchase_request")
    
    # Relationship from User
    users = relationship("Users", foreign_keys=[user_id], back_populates="purchase_request")
    
    def to_dict(self):
        return {
            "id": self.id,
            "pr_code": self.pr_code,
            "user_id": self.user_id,
            "division": self.division,
            "raw_material_id": self.raw_material_id,
            "quantity": self.quantity,
            "status" : self.pr_status,
            "metadata": {
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "is_deleted": self.is_deleted
            }
        }