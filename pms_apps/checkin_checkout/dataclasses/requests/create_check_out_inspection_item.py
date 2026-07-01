from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class CheckOutInspectionItemCreateRequest:
    check_out_id: int
    category: str
    item_name: str
    inspection_status: str
    severity: Optional[str] = None
    repair_status: Optional[str] = None
    item_approval_status: Optional[str] = None
    assigned_to_id: Optional[int] = None
    target_date: Optional[date] = None
    cost: Optional[float] = None
    photo: Optional[str] = None
    remarks: str = ""
    user_id: Optional[int] = None
