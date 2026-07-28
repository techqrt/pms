from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class CheckOutPaymentCreateRequest:
    check_out_id: int
    description: str
    amount: float
    tax: Optional[float] = None
    status: str = "Pending"
    charge_type: Optional[str] = None
    payment_method: Optional[str] = None
    payment_date: Optional[date] = None
    receipt_ref_no: Optional[str] = None
    remarks: str = ""
    user_id: Optional[int] = None
