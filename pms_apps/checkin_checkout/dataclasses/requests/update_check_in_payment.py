from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class CheckInPaymentUpdateRequest:
    check_in_payment_id: int
    description: Optional[str] = None
    amount: Optional[Decimal] = None
    status: Optional[str] = None
    payment_date: Optional[date] = None
    receipt_ref_no: Optional[str] = None
    remarks: Optional[str] = None
    user_id: Optional[int] = None


@dataclass
class CheckInPaymentDeleteRequest:
    check_in_payment_id: int
