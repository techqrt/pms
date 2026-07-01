from dataclasses import dataclass
from typing import Optional


@dataclass
class CheckOutKeyUpdateRequest:
    check_out_key_id: int
    key_number: Optional[str] = None
    key_type: Optional[str] = None
    status: Optional[str] = None
    remarks: Optional[str] = None
    user_id: Optional[int] = None


@dataclass
class CheckOutKeyDeleteRequest:
    check_out_key_id: int
