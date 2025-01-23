from enum import Enum

class SupplierType(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    
    @classmethod
    def get_all_supplier_type(cls):
        return [supplier_type.value for supplier_type in cls]