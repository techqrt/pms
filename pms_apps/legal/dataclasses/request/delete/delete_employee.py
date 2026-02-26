import dataclasses


@dataclasses.dataclass
class LegalEmployeeDeleteRequest:
    employee_id: int
