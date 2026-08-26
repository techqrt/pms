from dataclasses import dataclass


@dataclass
class BuildingCreateRequest:
    name: str
    address_line_1: str
    area_zone: str
    city: str
    state: str
    country: str
    pincode: str
    block: str | None = None
    total_floors: int | None = None
    year_of_construction: int | None = None
    address_line_2: str | None = None
    google_map_location: str | None = None
    internal_notes: str | None = None
    user_id: int | None = None
