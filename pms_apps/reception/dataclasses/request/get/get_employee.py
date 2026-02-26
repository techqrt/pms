import dataclasses

@dataclasses.dataclass
class ReceptionEmployeeGetRequest:
    employee_id: int
    values: str