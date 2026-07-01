from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class CheckOutInspectionItemUpdateRequest:
    check_out_inspection_item_id: int
    category: Optional[str] = None
    item_name: Optional[str] = None
    inspection_status: Optional[str] = None
    severity: Optional[str] = None
    repair_status: Optional[str] = None
    item_approval_status: Optional[str] = None
    assigned_to_id: Optional[int] = None
    target_date: Optional[date] = None
    cost: Optional[float] = None
    remarks: Optional[str] = None
    user_id: Optional[int] = None


@dataclass
class CheckOutInspectionItemDeleteRequest:
    check_out_inspection_item_id: int
