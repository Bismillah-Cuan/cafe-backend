from enum import Enum

class PRStatus(str, Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    REJECTED = "rejected"
    
    @classmethod
    def get_all_pr_status(cls):
        return [pr_status.value for pr_status in cls]