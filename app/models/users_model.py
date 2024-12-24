from app.connections.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from app.constant.enums.divisions import DivisionEnums

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    division = Column(Enum(DivisionEnums), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now(timezone.utc), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    # # relationship to purchase_order
    # purchase_order = relationship("PurchaseOrder", back_populates="users")
    
    # # relationship to purchase_request
    purchase_request = relationship("PurchaseRequest", back_populates="users")
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
    
    def to_dict(self):
        user = {
            "id": self.id,
            "username": self.username,
            "division": self.division,
            "metadata": {
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "is_deleted": self.is_deleted
            }
        }
        
        return user