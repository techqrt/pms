from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


@dataclass
class CheckInInformationUpdateRequest:
    check_in_id: int
    assigned_employee_id: Optional[int] = None
    check_in_date: Optional[date] = None
    check_in_status: Optional[str] = None
    remarks_notes: Optional[str] = None


@dataclass
class CheckInTenantDetailsUpdateRequest:
    check_in_id: int
    tenant_code: Optional[str] = None
    tenant_name: Optional[str] = None
    tenant_type: Optional[str] = None
    tenant_mobile_number: Optional[str] = None
    tenant_email: Optional[str] = None
    tenant_civil_id: Optional[str] = None
    tenant_passport_number: Optional[str] = None
    tenant_nationality: Optional[str] = None
    tenant_address: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    marital_status: Optional[str] = None
    alternate_mobile_number: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_number: Optional[str] = None
    profession: Optional[str] = None
    company_name: Optional[str] = None
    move_in_reason: Optional[str] = None
    number_of_occupants: Optional[int] = None


@dataclass
class CheckInPropertyDetailsUpdateRequest:
    check_in_id: int
    property_type: Optional[str] = None
    property_code: Optional[str] = None
    building_name: Optional[str] = None
    flat_unit_number: Optional[str] = None
    floor_number: Optional[str] = None
    property_status: Optional[str] = None


@dataclass
class CheckInRentalDetailsUpdateRequest:
    check_in_id: int
    monthly_rent: Optional[Decimal] = None
    security_deposit: Optional[Decimal] = None
    advance_rent_received: Optional[Decimal] = None
    first_month_rent_paid: Optional[Decimal] = None
    payment_mode: Optional[str] = None
    maintenance_charges: Optional[Decimal] = None


@dataclass
class CheckInPropertyInspectionUpdateRequest:
    check_in_id: int
    inspection_required: Optional[str] = None
    inspection_date: Optional[date] = None
    technician_type: Optional[str] = None
    manager_approval: Optional[str] = None
    issue_identified: Optional[str] = None
    supervisor_remarks: Optional[str] = None
    inspection_priority: Optional[str] = None
    inspection_type: Optional[str] = None
    inspection_duration: Optional[str] = None
    next_inspection_due: Optional[date] = None


@dataclass
class CheckInRepairApprovalUpdateRequest:
    check_in_id: int
    repair_required: Optional[str] = None
    quotation_amount: Optional[Decimal] = None
    inventory_available: Optional[str] = None
    gm_approval: Optional[str] = None
    landlord_consent: Optional[str] = None
    finance_alert_generated: Optional[str] = None
    rent_adjustment_amount: Optional[Decimal] = None
    repair_priority: Optional[str] = None
    recommended_by_id: Optional[int] = None
    approved_by_id: Optional[int] = None
    approved_on: Optional[date] = None
    inspector_comments: Optional[str] = None


@dataclass
class CheckInUtilityMeterReadingsUpdateRequest:
    check_in_id: int
    electricity_meter_reading: Optional[Decimal] = None
    water_meter_reading: Optional[Decimal] = None
    gas_meter_reading: Optional[Decimal] = None
    utility_adjustment_amount: Optional[Decimal] = None


@dataclass
class CheckInAgreementDetailsUpdateRequest:
    check_in_id: int
    agreement_type: Optional[str] = None
    agreement_status: Optional[str] = None
    agreement_start_date: Optional[date] = None
    agreement_end_date: Optional[date] = None
    agreement_document: Optional[str] = None
    agreement_template: Optional[str] = None
    agreement_number: Optional[str] = None
    generated_on: Optional[datetime] = None
    generated_by_id: Optional[int] = None
    submitted_to_tenant_on: Optional[datetime] = None
    tenant_signed_on: Optional[datetime] = None
    manager_signed_on: Optional[datetime] = None
    signed_by_id: Optional[int] = None
    renewal_reminder_date: Optional[date] = None
    auto_reminder_enabled: Optional[bool] = None
    agreement_notes: Optional[str] = None


@dataclass
class CheckInKeyHandoverUpdateRequest:
    check_in_id: int
    key_number: Optional[str] = None
    key_type: Optional[str] = None
    key_available: Optional[str] = None
    key_booking_date: Optional[date] = None
    confirmation_received: Optional[str] = None
    key_delivery_date: Optional[date] = None
    key_handover_status: Optional[str] = None
    expected_handover_date: Optional[datetime] = None
    handover_notes: Optional[str] = None
    tenant_confirmation_notes: Optional[str] = None
    key_booked_on: Optional[datetime] = None
    key_booked_by_id: Optional[int] = None
    key_prepared_on: Optional[datetime] = None
    key_notified_on: Optional[datetime] = None
    handover_completed_on: Optional[datetime] = None
    handed_over_by_id: Optional[int] = None


@dataclass
class CheckInCommentsUpdateRequest:
    check_in_id: int
    internal_comments: Optional[str] = None
    tenant_remarks: Optional[str] = None
    special_instructions: Optional[str] = None
