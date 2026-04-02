from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class PropertyAssignmentCreateRequest:
    property_id: int
    tenant_id: int
    assigned_by_id: int
    assignment_status: str = "Pending"
    tenant_type: str = "Individual"
    company_name: Optional[str] = None
    rental_start_date: Optional[date] = None
    rental_end_date: Optional[date] = None
    agreement_duration_months: Optional[int] = None
    maintenance_charges: Optional[Decimal] = None
    advance_rent_paid: bool = False
    payment_mode: Optional[str] = None
    agreement_type: Optional[str] = None
    agreement_status: str = "Pending"
    agreement_prepared_by_id: Optional[int] = None
    key_available_in_office: str = "No"
    key_code: Optional[str] = None
    key_handover_date: Optional[date] = None
    key_handover_status: str = "Pending"
    electricity_meter_number: Optional[str] = None
    electricity_meter_reading_start: Optional[Decimal] = None
    water_meter_reading_start: Optional[Decimal] = None
    gas_meter_reading_start: Optional[Decimal] = None
    finance_approval_status: str = "Pending"
    rent_entry_created: str = "No"
    invoice_generated: str = "No"
    maintenance_required: str = "No"
    maintenance_ticket_id: Optional[str] = None
    maintenance_status: str = "Pending"
    internal_notes: str = ""
    tenant_special_requirements: str = ""
