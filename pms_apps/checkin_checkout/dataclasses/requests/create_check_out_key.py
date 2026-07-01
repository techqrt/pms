from dataclasses import dataclass
from typing import Optional


@dataclass
class CheckOutKeyCreateRequest:
    check_out_id: int
    key_number: str
    key_type: str
    status: str = "Pending"
    remarks: str = ""
    user_id: Optional[int] = None
