import dataclasses


@dataclasses.dataclass
class LegalEmployeeUpdateRequest:
    employee_id: int
    name: str
    dob: str
    designation: str
    active_cases: int
    case_specialization: str
    manager_ref: int
