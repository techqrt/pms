from dataclasses import dataclass
from typing import List


@dataclass
class PropertyCreateRequest:
    block : str
    building_details: str
    floor: str
    flat_number: int
    dimension_length_ft: float
    dimension_breadth_ft: float
    dimension_area_sqft: float
    rental_type: str
    hall: bool
    bedroom_count: int
    kitchen: bool
    attached_bathroom_count: int
    single_bathroom_count: int
    balcony: bool
    store_room: bool
    rental_for: str
    advance_amount_rent: int
    expected_rent: float
    agreement_id: int
    photos: List[str]
    videos: List[str]
