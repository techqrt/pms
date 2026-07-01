from dataclasses import dataclass
from typing import Optional


@dataclass
class CheckOutUtilityReadingUpdateRequest:
    check_out_utility_reading_id: int
    utility_type: Optional[str] = None
    meter_no: Optional[str] = None
    reading_value: Optional[float] = None
    consumption: Optional[float] = None
    unit: Optional[str] = None
    rate_per_unit: Optional[float] = None
    charges: Optional[float] = None
    status: Optional[str] = None
    remarks: Optional[str] = None
    user_id: Optional[int] = None


@dataclass
class CheckOutUtilityReadingDeleteRequest:
    check_out_utility_reading_id: int
