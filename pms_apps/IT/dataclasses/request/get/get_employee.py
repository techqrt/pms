import dataclasses

@dataclasses.dataclass
class ITEmployeeGetRequest:
    employee_id: int
    values: str
