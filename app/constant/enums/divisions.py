from enum import Enum

class DivisionEnums(str, Enum):
    ADMIN = "admin"
    KITCHEN = "kitchen"
    FINANCE = "finance"
    BAR = "bar"
    SOSMED = "sosmed"
    SUPER_ADMIN = "super_admin"
    
    @classmethod
    def get_all_division(cls):
        divisions = list(cls)
        divisions_value = {division.value for division  in divisions}
        
        return divisions_value