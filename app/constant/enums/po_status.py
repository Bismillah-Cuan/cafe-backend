from enum import Enum

class POStatus(str, Enum):
    ON_PROCESS = "on_process"
    PURCHASED = "purchased"
    RECEIVED = "received"
    ISSUES_REQUESTED = "issues_requested"
    ISSUES_ACCEPTED = "issues_accepted"
    DONE = "done"
    
    @classmethod
    def get_all_po_status(cls):
        return [po_status.value for po_status in cls]