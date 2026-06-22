from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class CheckInPaymentCreateRequest:
    check_in_id: int
    description: str
    amount: Decimal
    status: str = "Pending"
    payment_date: Optional[date] = None
    receipt_ref_no: Optional[str] = None
    remarks: str = ""
    user_id: Optional[int] = None
