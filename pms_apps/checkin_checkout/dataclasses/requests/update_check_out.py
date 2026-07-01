from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class CheckOutInformationUpdateRequest:
    check_out_id: int
    assigned_employee_id: Optional[int] = None
    check_out_date: Optional[date] = None
    check_out_status: Optional[str] = None
    remarks_notes: Optional[str] = None
    request_from: Optional[str] = None


@dataclass
class CheckOutTenantDetailsUpdateRequest:
    check_out_id: int
    tenant_code: Optional[str] = None
    tenant_name: Optional[str] = None
    tenant_type: Optional[str] = None
    tenant_mobile_number: Optional[str] = None
    tenant_email: Optional[str] = None
    tenant_civil_id: Optional[str] = None
    tenant_passport_number: Optional[str] = None
    tenant_nationality: Optional[str] = None
    tenant_address: Optional[str] = None


@dataclass
class CheckOutPropertyDetailsUpdateRequest:
    check_out_id: int
    property_type: Optional[str] = None
    property_code: Optional[str] = None
    building_name: Optional[str] = None
    flat_unit_number: Optional[str] = None
    floor_number: Optional[str] = None
    property_status: Optional[str] = None


@dataclass
class CheckOutRentalDetailsUpdateRequest:
    check_out_id: int
    monthly_rent: Optional[Decimal] = None
    security_deposit: Optional[Decimal] = None
    advance_rent_received: Optional[Decimal] = None
    first_month_rent_paid: Optional[Decimal] = None
    payment_mode: Optional[str] = None
    maintenance_charges: Optional[Decimal] = None


@dataclass
class CheckOutPropertyInspectionUpdateRequest:
    check_out_id: int
    inspection_required: Optional[str] = None
    inspection_date: Optional[date] = None
    technician_type: Optional[str] = None
    manager_approval: Optional[str] = None
    inspection_priority: Optional[str] = None
    issue_identified: Optional[str] = None
    supervisor_remarks: Optional[str] = None


@dataclass
class CheckOutRepairDamageUpdateRequest:
    check_out_id: int
    repair_required: Optional[str] = None
    quotation_amount: Optional[Decimal] = None
    inventory_available: Optional[str] = None
    gm_approval: Optional[str] = None
    landlord_consent: Optional[str] = None
    finance_alert_generated: Optional[str] = None
    rent_adjustment_amount: Optional[Decimal] = None
    repair_priority: Optional[str] = None


@dataclass
class CheckOutUtilityMeterReadingsUpdateRequest:
    check_out_id: int
    electricity_meter_reading: Optional[Decimal] = None
    water_meter_reading: Optional[Decimal] = None
    gas_meter_reading: Optional[Decimal] = None


@dataclass
class CheckOutFinanceDetailsUpdateRequest:
    check_out_id: int
    charge_type: Optional[str] = None
    total_amount: Optional[Decimal] = None
    payment_status: Optional[str] = None
    payment_date: Optional[date] = None
    transaction_id: Optional[str] = None
    settlement_status: Optional[str] = None
    finance_description: Optional[str] = None
    payment_proof: Optional[str] = None


@dataclass
class CheckOutKeyReturnUpdateRequest:
    check_out_id: int
    key_number: Optional[str] = None
    key_type: Optional[str] = None
    key_available: Optional[str] = None
    key_return: Optional[str] = None
    expected_return_date: Optional[date] = None
    confirmation_received: Optional[str] = None
    key_return_date: Optional[date] = None
    key_return_status: Optional[str] = None


@dataclass
class CheckOutCommentsUpdateRequest:
    check_out_id: int
    internal_comments: Optional[str] = None
    tenant_remarks: Optional[str] = None
    special_instructions: Optional[str] = None
