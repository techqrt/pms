from dataclasses import dataclass
from typing import Optional


@dataclass
class CheckInRequestRespondRequest:
    check_in_id: int
    accept: bool = False
    reject: bool = False
    rejection_reason: Optional[str] = None
