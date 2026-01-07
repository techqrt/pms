import dataclasses

@dataclasses.dataclass
class CollectionEmployeeUpdateRequest:
    employee_id: int
    name: str
    dob: str
    designation: str
    region: str
    collections_made: float
    overdue_accounts_handled: int
    manager_ref: int