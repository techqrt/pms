import dataclasses

@dataclasses.dataclass
class FinanceEmployeeUpdateRequest:
    employee_id: int
    name: str
    dob: str
    role_title: str
    invoices_processed: int
    payments_verified: int
    total_amount_handled: float
    manager_ref: int