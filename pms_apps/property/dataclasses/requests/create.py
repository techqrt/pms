from dataclasses import dataclass
from typing import Optional, List
from pms_apps.authentication.dataclasses.request.create import PropertyUserRequest


@dataclass
class PropertyCreateRequest:
    block : Optional[str] = None
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
    created_by: Optional[PropertyUserRequest] = None
    assigned_to: Optional[PropertyUserRequest] = None

