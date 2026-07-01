from dataclasses import dataclass
from typing import Optional


@dataclass
class CheckOutUtilityReadingCreateRequest:
    check_out_id: int
    utility_type: str
    meter_no: Optional[str] = None
    reading_value: Optional[float] = None
    consumption: Optional[float] = None
    unit: Optional[str] = None
    rate_per_unit: Optional[float] = None
    charges: Optional[float] = None
    status: str = "Normal"
    remarks: str = ""
    user_id: Optional[int] = None
