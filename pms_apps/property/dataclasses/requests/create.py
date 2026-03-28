from dataclasses import dataclass
from typing import List

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


@dataclass
class PropertyCommonData:
    building_name: str
    total_floors: int
    carpet_area_sqft: Decimal
    builtup_area_sqft: Decimal
    monthly_rent: Decimal
    security_deposit_amount: Decimal
    electricity_charge_type: str
    water_charge_type: str
    late_fee_type: str
    late_fee_value: Decimal
    current_status: str
    landlord_id: int
    created_by_id: int
    address_line_1: str
    area_zone: str
    city: str
    state: str
    country: str
    pincode: str
    google_map_location: str
    year_of_construction: int
    address_line_2: str
    internal_notes: str
    other_charges: dict | None = None
    available_from: date | None = None
    current_tenant_id: int | None = None


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


@dataclass
class FlatPropertyData:
    flat_number: str
    flat_configuration: str
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


@dataclass
class PropertyCreateRequest:
    rental_type: str
    rental_for: str
    property_details: PropertyCommonData
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
    assigned_to: dict | None = None
    photos: List[str] = field(default_factory=list)
    videos: List[str] = field(default_factory=list)
    user_id: int | None = None
