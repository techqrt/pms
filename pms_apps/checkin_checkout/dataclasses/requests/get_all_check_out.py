from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class CheckOutGetAllRequest:
    values: str
    page_num: int
    limit: int
    sort_by: str
    sort_order: str
    search_key: str
    status: List[str]
    assigned_employee_id: List[str]
    manager_approval: List[str]
    key_return_status: List[str]
    payment_status: List[str]
    request_from: List[str]
    building: str = ''
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    present_url: str = None
