from dataclasses import dataclass
from typing import List

@dataclass
class PropertyUpdateRequest:
    property_id: int
    block : str = None
    building_details: str = None
    floor: str = None
    flat_number: int = None
    dimension_length_ft: float = None
    dimension_breadth_ft: float = None
    dimension_area_sqft: float = None
    rental_type: str = None
    hall: bool = None
    bedroom_count: int = None
    kitchen: bool = None
    attached_bathroom_count: int = None
    single_bathroom_count: int = None
    balcony: bool = None
    store_room: bool = None
    rental_for: str = None
    advance_amount_rent: int = None
    expected_rent: float = None
    agreement_id: int = None
    photos: List[str] = None
    videos: List[str] = None
    assigned_to: int = None
