from dataclasses import dataclass


@dataclass
class BuildingCreateRequest:
    name: str
    property_type: str
    address_line_1: str
    area_zone: str
    city: str
    state: str
    country: str
    pincode: str
    block: str | None = None
    total_floors: int | None = None
    year_of_construction: int | None = None
    facilities: list | None = None
    rental_purpose: str | None = None
    allowed_tenant_types: list | None = None
    parking: bool | None = None
    lift: bool | None = None
    security: bool | None = None
    gas_pipeline: bool | None = None
    water_supply: bool | None = None
    intercom: bool | None = None
    fire_safety: bool | None = None
    project_name: str | None = None
    private_garden: bool | None = None
    private_parking: str | None = None
    swimming_pool: str | None = None
    terrace_access: bool | None = None
    boundary_wall: bool | None = None
    driveway: bool | None = None
    water_supply_24x7: bool | None = None
    security_guard: bool | None = None
    clubhouse_access: bool | None = None
    gym: bool | None = None
    childrens_play_area: bool | None = None
    internal_roads: bool | None = None
    street_lights: bool | None = None
    gated_community: bool | None = None
    power_backup: bool | None = None
    commercial_category: str | None = None
    lift_type: str | None = None
    fire_safety_compliant: bool | None = None
    emergency_exit: bool | None = None
    parking_availability: str | None = None
    cctv: bool | None = None
    warehouse_category: str | None = None
    industrial_estate_name: str | None = None
    ownership_type: str | None = None
    has_transformer: bool | None = None
    water_supply_source: str | None = None
    has_drainage_system: bool | None = None
    has_internet_fiber: bool | None = None
    allowed_industry_types: list | None = None
    power_load_kw: float | None = None
    has_dg_backup: bool | None = None
    address_line_2: str | None = None
    google_map_location: str | None = None
    internal_notes: str | None = None
    user_id: int | None = None
