from dataclasses import dataclass
from typing import Optional, List

@dataclass
class PropertyUpdateRequest:
    property_id: int
    building_details: Optional[str] = None
    floor: Optional[str] = None
    flat_number: Optional[int] = None
    dimension_length_ft: Optional[float] = None
    dimension_breadth_ft: Optional[float] = None
    dimension_area_sqft: Optional[float] = None
    rental_type: Optional[str] = None
    hall: Optional[bool] = None
    bedroom_count: Optional[int] = None
    kitchen: Optional[bool] = None
    attached_bathroom_count: Optional[int] = None
    single_bathroom_count: Optional[int] = None
    balcony: Optional[bool] = None
    store_room: Optional[bool] = None
    rental_for: Optional[str] = None
    advance_amount_rent: Optional[int] = None
    expected_rent: Optional[float] = None
    agreement_id: Optional[int] = None
    photos: Optional[List[str]] = None
    videos: Optional[List[str]] = None
    assigned_to: Optional[int] = None
    is_active: Optional[bool] = None


