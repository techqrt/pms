import dataclasses

@dataclasses.dataclass
class LegalEmployeeGetRequest:
    employee_id: int
    values: str