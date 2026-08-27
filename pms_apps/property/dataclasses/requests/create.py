from dataclasses import dataclass
from typing import List

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


@dataclass
class PropertyCommonData:
    monthly_rent: Decimal
    security_deposit_amount: Decimal
    late_fee_type: str
    late_fee_value: Decimal
    current_status: str
    landlord_id: int
    created_by_id: int
    # Required when building_id is not supplied at the top level; otherwise
    # auto-populated from the linked Building (see PropertyCreateSerializer.validate).
    building_name: str | None = None
    unit_number: str | None = None
    rental_purpose: str | None = None
    address_line_1: str | None = None
    area_zone: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    pincode: str | None = None
    total_floors: int | None = None
    carpet_area_sqft: Decimal | None = None
    builtup_area_sqft: Decimal | None = None
    google_map_location: str | None = None
    year_of_construction: int | None = None
    address_line_2: str | None = None
    internal_notes: str | None = None
    electricity_charge_type: str | None = None
    water_charge_type: str | None = None
    other_charges: dict | None = None
    available_from: date | None = None
    current_tenant_id: str | None = None
    furnishing_status: str | None = None
    payment_due_date: date | None = None
    rent_increase_date: date | None = None


@dataclass
class CommercialPropertyData:
    commercial_category: str
    floor_number: int | None = None
    frontage_width_ft: Decimal | None = None
    ceiling_height_ft: Decimal | None = None
    no_of_cabins: int | None = None
    no_of_washrooms: int | None = None
    loading_area: str | None = None
    power_load_kw: Decimal | None = None
    has_dg_backup: bool | None = None
    lift_type: str | None = None
    fire_safety_compliant: bool | None = None
    emergency_exit: bool | None = None
    parking_availability: str | None = None
    commercial_maintenance_charge_type: str | None = None
    maintenance_charge_amount: Decimal | None = None
    electricity_charge_amount: Decimal | None = None
    water_charge_amount: Decimal | None = None
    gst_applicable: bool | None = None
    gst_percentage: Decimal | None = None
    security_deposit_months: int | None = None
    lease_type: str | None = None
    lease_tenure_years: int | None = None
    lock_in_period_months: int | None = None
    allowed_business: str | None = None
    prohibited_business: str | None = None
    cctv: bool | None = None
    super_builtup_area_sqft: Decimal | None = None
    pantry: bool | None = None
    store_room: bool | None = None


@dataclass
class FlatPropertyData:
    flat_configuration: str
    flat_number: str | None = None
    floor_number: int | None = None
    building_block: str | None = None
    no_of_bathrooms: int | None = None
    kitchen_type: str | None = None
    facing: str | None = None
    balcony: bool | None = None
    parking: bool | None = None
    lift: bool | None = None
    security: bool | None = None
    gas_pipeline: bool | None = None
    water_supply: bool | None = None
    power_backup: bool | None = None
    cctv: bool | None = None
    intercom: bool | None = None
    fire_safety: bool | None = None
    allowed_tenant_types: List[str] | None = None
    store_room: bool | None = None
    maintenance_charge_amount: Decimal | None = None
    electricity_charge_amount: Decimal | None = None
    water_charge_amount: Decimal | None = None


@dataclass
class VillaPropertyData:
    villa_name: str
    villa_type: str
    villa_configuration: str
    project_name: str | None = None
    plot_area_sqft: Decimal | None = None
    number_of_bedrooms: int | None = None
    number_of_bathrooms: int | None = None
    living_rooms_count: int | None = None
    store_room: bool | None = None
    servant_room: bool | None = None
    balcony_or_sitout: bool | None = None
    private_garden: bool | None = None
    terrace_access: bool | None = None
    boundary_wall: bool | None = None
    driveway: bool | None = None
    private_parking: str | None = None
    villa_maintenance_charge_type: str | None = None
    gardening_charges: Decimal | None = None
    water_supply_24x7: bool | None = None
    security_guard: bool | None = None
    clubhouse_access: bool | None = None
    gym: bool | None = None
    childrens_play_area: bool | None = None
    internal_roads: bool | None = None
    street_lights: bool | None = None
    gated_community: bool | None = None
    bachelor_allowed: bool | None = None
    pets_allowed: bool | None = None
    power_backup: bool | None = None
    cctv: bool | None = None
    allowed_tenant_types: List[str] | None = None
    maintenance_charge_amount: Decimal | None = None
    electricity_charge_amount: Decimal | None = None
    water_charge_amount: Decimal | None = None
    facing: str | None = None
    kitchen_type: str | None = None
    swimming_pool: str | None = None
    unit: str | None = None
    super_builtup_area_sqft: Decimal | None = None
    pantry: bool | None = None


@dataclass
class WarehousePropertyData:
    warehouse_category: str
    warehouse_name: str
    plot_area_sqft: Decimal
    clear_height_ft: Decimal
    no_of_bays: int
    no_of_loading_docks: int
    dock_height_ft: Decimal
    floor_load_capacity_mt_sqft: str
    column_spacing_ft: Decimal
    has_mezzanine_floor: bool
    power_load_kw: Decimal
    has_transformer: bool
    has_dg_backup: bool
    water_supply_source: str
    has_drainage_system: bool
    has_internet_fiber: bool
    entry_gate_width_ft: Decimal
    road_width_ft: Decimal
    truck_parking_capacity: int
    container_access: str
    turning_radius: str
    has_weighbridge_nearby: bool
    monthly_rent_type: str
    rent_escalation_percentage: Decimal | None = None
    lock_in_period_months: int | None = None
    allowed_industry_types: List[str] | None = None
    industrial_estate_name: str | None = None
    plot_shed_number: str | None = None
    ownership_type: str | None = None
    office_space_area_sqft: Decimal | None = None
    maintenance_charges: Decimal | None = None
    cam_charges: Decimal | None = None
    security_deposit_months: int | None = None
    security_deposit_amount: Decimal | None = None
    security_deposit_type: str | None = None
    loading_area: str | None = None


@dataclass
class PropertyCreateRequest:
    rental_type: str
    rental_for: str
    property_details: PropertyCommonData
    building_id: int | None = None
    block: str | None = None
    building_details: str | None = None
    floor: str | None = None
    flat_number: int | None = None
    dimension_length_ft: Decimal | None = None
    dimension_breadth_ft: Decimal | None = None
    dimension_area_sqft: Decimal | None = None
    advance_amount_rent: int | None = None
    expected_rent: Decimal | None = None
    agreement_id: int | None = None
    commercial_data: CommercialPropertyData | None = None
    flat_data: FlatPropertyData | None = None
    villa_data: VillaPropertyData | None = None
    warehouse_data: WarehousePropertyData | None = None
    assigned_to: dict | None = None
    photos: List[str] = field(default_factory=list)
    videos: List[str] = field(default_factory=list)
    user_id: int | None = None
