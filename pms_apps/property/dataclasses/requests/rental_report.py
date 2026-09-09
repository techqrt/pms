from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from pms.config import Configurations


@dataclass
class RentalReportRequest:
    page_num: int
    limit: int
    search: str
    property_types: List[str]
    rental_for: List[str]
    statuses: List[str]
    bedrooms: List[str]
    features: List[str]
    city: str
    min_rent: Optional[float] = None
    max_rent: Optional[float] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    present_url: str = None

    def __post_init__(self):
        self.limit = min(self.limit, Configurations.max_pagination_limit)
