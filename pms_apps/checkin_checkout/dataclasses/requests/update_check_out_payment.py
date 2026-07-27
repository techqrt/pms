from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class CheckOutPaymentUpdateRequest:
    check_out_payment_id: int
    description: Optional[str] = None
    amount: Optional[float] = None
    tax: Optional[float] = None
    status: Optional[str] = None
    payment_method: Optional[str] = None
    payment_date: Optional[date] = None
    receipt_ref_no: Optional[str] = None
    remarks: Optional[str] = None
    user_id: Optional[int] = None


@dataclass
class CheckOutPaymentDeleteRequest:
    check_out_payment_id: int
