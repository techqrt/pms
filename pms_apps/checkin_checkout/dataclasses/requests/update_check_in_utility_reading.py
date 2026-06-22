from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class CheckInUtilityReadingUpdateRequest:
    check_in_utility_reading_id: int
    utility_type: Optional[str] = None
    meter_no: Optional[str] = None
    reading_value: Optional[Decimal] = None
    consumption: Optional[Decimal] = None
    unit: Optional[str] = None
    rate_per_unit: Optional[Decimal] = None
    charges: Optional[Decimal] = None
    status: Optional[str] = None
    remarks: Optional[str] = None
    user_id: Optional[int] = None


@dataclass
class CheckInUtilityReadingDeleteRequest:
    check_in_utility_reading_id: int
