import dataclasses

@dataclasses.dataclass
class MaintenanceEmployeeGetRequest:
    employee_id: int
    values: str