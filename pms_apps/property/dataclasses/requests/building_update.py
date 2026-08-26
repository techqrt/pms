from dataclasses import dataclass
from typing import Optional


@dataclass
class BuildingUpdateRequest:
    building_id: int
    name: Optional[str] = None
    block: Optional[str] = None
    total_floors: Optional[int] = None
    year_of_construction: Optional[int] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    area_zone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    google_map_location: Optional[str] = None
    internal_notes: Optional[str] = None
    user_id: Optional[int] = None
