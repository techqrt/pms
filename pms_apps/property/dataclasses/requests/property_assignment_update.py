from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class PropertyAssignmentUpdateRequest:
    property_assignment_id: int
    assignment_status: Optional[str] = None
    tenant_type: Optional[str] = None
    company_name: Optional[str] = None
    rental_start_date: Optional[date] = None
    rental_end_date: Optional[date] = None
    agreement_duration_months: Optional[int] = None
    maintenance_charges: Optional[Decimal] = None
    advance_rent_paid: Optional[bool] = None
    payment_mode: Optional[str] = None
    agreement_type: Optional[str] = None
    agreement_status: Optional[str] = None
    agreement_prepared_by_id: Optional[int] = None
    key_available_in_office: Optional[str] = None
    key_code: Optional[str] = None
    key_handover_date: Optional[date] = None
    key_handover_status: Optional[str] = None
    electricity_meter_number: Optional[str] = None
    electricity_meter_reading_start: Optional[Decimal] = None
    water_meter_reading_start: Optional[Decimal] = None
    gas_meter_reading_start: Optional[Decimal] = None
    finance_approval_status: Optional[str] = None
    rent_entry_created: Optional[str] = None
    invoice_generated: Optional[str] = None
    maintenance_required: Optional[str] = None
    maintenance_ticket_id: Optional[str] = None
    maintenance_status: Optional[str] = None
    internal_notes: Optional[str] = None
    tenant_special_requirements: Optional[str] = None
