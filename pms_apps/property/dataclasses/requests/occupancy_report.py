from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class OccupancyReportRequest:
    page_num: int
    limit: int
    search: str
    property_types: List[str]
    statuses: List[str]
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    present_url: str = None
