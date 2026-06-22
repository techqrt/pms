from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class CheckInUtilityReadingCreateRequest:
    check_in_id: int
    utility_type: str
    meter_no: Optional[str] = None
    reading_value: Optional[Decimal] = None
    consumption: Optional[Decimal] = None
    unit: Optional[str] = None
    rate_per_unit: Optional[Decimal] = None
    charges: Optional[Decimal] = None
    status: str = "Normal"
    remarks: str = ""
    user_id: Optional[int] = None
