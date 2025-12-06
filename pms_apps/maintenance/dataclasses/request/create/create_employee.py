import dataclasses

@dataclasses.dataclass
class MaintenanceEmployeeCreateRequest:
    employee_id: int
    name: str
    dob: str
    designation: str
    specialization: str
    assigned_tasks: int
    manager_ref: int