from enum import Enum

class RawMaterialTypeEnums(Enum):
    DRY = "dry"
    FRESH = "fresh"
    DAIRY = "dairy"
    ATK = "atk"
    PACKAGING = "packaging"
    SUPPORT = "support"
    
    @classmethod
    def get_all_raw_material_types(cls):
        return [raw_material_type.value for raw_material_type in cls]