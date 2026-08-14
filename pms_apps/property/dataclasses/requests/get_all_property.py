from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class PropertyGetAllRequest:
    values: str
    page_num: int
    limit: int
    sort_by: str
    sort_order: str
    search_key: str
    property_types: List[str]
    rental_for: List[str]
    bedrooms: List[str]
    features: List[str]
    city: str = ''
    min_rent: Optional[float] = None
    max_rent: Optional[float] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    present_url: str = None
