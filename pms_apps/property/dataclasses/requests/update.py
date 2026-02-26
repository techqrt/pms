from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import date
from decimal import Decimal

@dataclass
class PropertyDetailUpdateData:
    building_name: Optional[str] = None
    total_floors: Optional[int] = None
    carpet_area_sqft: Optional[Decimal] = None
    builtup_area_sqft: Optional[Decimal] = None
    monthly_rent: Optional[Decimal] = None
    security_deposit_amount: Optional[Decimal] = None
    electricity_charge_type: Optional[str] = None
    water_charge_type: Optional[str] = None
    late_fee_type: Optional[str] = None
    late_fee_value: Optional[Decimal] = None
    current_status: Optional[str] = None
    landlord_id: Optional[int] = None
    address_line_1: Optional[str] = None
    area_zone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    google_map_location: Optional[str] = None
    year_of_construction: Optional[int] = None
    other_charges: Optional[Dict] = None
    available_from: Optional[date] = None
    current_tenant_id: Optional[int] = None
    address_line_2: Optional[str] = None
    internal_notes: Optional[str] = None

@dataclass
class CommercialPropertyUpdateData:
    commercial_category: Optional[str] = None
    floor_number: Optional[int] = None
    frontage_width_ft: Optional[Decimal] = None
    ceiling_height_ft: Optional[Decimal] = None
    no_of_cabins: Optional[int] = None
    no_of_washrooms: Optional[int] = None
    loading_area: Optional[str] = None
    power_load_kw: Optional[Decimal] = None
    has_dg_backup: Optional[bool] = None
    lift_type: Optional[str] = None
    fire_safety_compliant: Optional[bool] = None
    emergency_exit: Optional[bool] = None
    parking_availability: Optional[str] = None
    commercial_maintenance_charge_type: Optional[str] = None
    maintenance_charge_amount: Optional[Decimal] = None
    gst_applicable: Optional[bool] = None
    gst_percentage: Optional[Decimal] = None
    security_deposit_months: Optional[int] = None
    lease_type: Optional[str] = None
    lease_tenure_years: Optional[int] = None
    lock_in_period_months: Optional[int] = None
    allowed_business: Optional[str] = None
    prohibited_business: Optional[str] = None

@dataclass
class FlatPropertyUpdateData:
    flat_number: Optional[str] = None
    flat_configuration: Optional[str] = None
    floor_number: Optional[int] = None
    building_block: Optional[str] = None
    no_of_bathrooms: Optional[int] = None
    kitchen_type: Optional[str] = None
    facing: Optional[str] = None
    balcony: Optional[bool] = None
    parking: Optional[bool] = None
    lift: Optional[bool] = None
    security: Optional[bool] = None
    gas_pipeline: Optional[bool] = None
    water_supply: Optional[bool] = None
    power_backup: Optional[bool] = None
    cctv: Optional[bool] = None
    intercom: Optional[bool] = None
    fire_safety: Optional[bool] = None
    allowed_tenant_types: Optional[List[str]] = None
    store_room: Optional[bool] = None
    maintenance_charge_amount: Optional[Decimal] = None

@dataclass
class VillaPropertyUpdateData:
    villa_name: Optional[str] = None
    villa_type: Optional[str] = None
    villa_configuration: Optional[str] = None
    project_name: Optional[str] = None
    plot_area_sqft: Optional[Decimal] = None
    number_of_bedrooms: Optional[int] = None
    number_of_bathrooms: Optional[int] = None
    living_rooms_count: Optional[int] = None
    store_room: Optional[bool] = None
    servant_room: Optional[bool] = None
    balcony_or_sitout: Optional[bool] = None
    private_garden: Optional[bool] = None
    terrace_access: Optional[bool] = None
    boundary_wall: Optional[bool] = None
    driveway: Optional[bool] = None
    private_parking: Optional[str] = None
    villa_maintenance_charge_type: Optional[str] = None
    gardening_charges: Optional[Decimal] = None
    water_supply_24x7: Optional[bool] = None
    security_guard: Optional[bool] = None
    clubhouse_access: Optional[bool] = None
    gym: Optional[bool] = None
    childrens_play_area: Optional[bool] = None
    internal_roads: Optional[bool] = None
    street_lights: Optional[bool] = None
    gated_community: Optional[bool] = None
    bachelor_allowed: Optional[bool] = None
    pets_allowed: Optional[bool] = None
    power_backup: Optional[bool] = None
    cctv: Optional[bool] = None
    allowed_tenant_types: Optional[List[str]] = None
    maintenance_charge_amount: Optional[Decimal] = None

@dataclass
class PropertyUpdateRequest:
    property_id: int
    block: Optional[str] = None
    building_details: Optional[str] = None
    floor: Optional[str] = None
    flat_number: Optional[int] = None
    dimension_length_ft: Optional[Decimal] = None
    dimension_breadth_ft: Optional[Decimal] = None
    dimension_area_sqft: Optional[Decimal] = None
    rental_type: Optional[str] = None
    rental_for: Optional[str] = None
    advance_amount_rent: Optional[int] = None
    expected_rent: Optional[Decimal] = None
    agreement_id: Optional[int] = None
    property_details: Optional[PropertyDetailUpdateData] = None
    commercial_data: Optional[CommercialPropertyUpdateData] = None
    flat_data: Optional[FlatPropertyUpdateData] = None
    villa_data: Optional[VillaPropertyUpdateData] = None
    assigned_to: Optional[int] = None
    photos: Optional[List[str]] = None
    videos: Optional[List[str]] = None
