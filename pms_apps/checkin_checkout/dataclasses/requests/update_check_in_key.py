from dataclasses import dataclass
from typing import Optional


@dataclass
class CheckInKeyUpdateRequest:
    check_in_key_id: int
    key_number: Optional[str] = None
    key_type: Optional[str] = None
    status: Optional[str] = None
    remarks: Optional[str] = None
    user_id: Optional[int] = None


@dataclass
class CheckInKeyDeleteRequest:
    check_in_key_id: int
