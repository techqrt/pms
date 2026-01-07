import dataclasses

@dataclasses.dataclass
class ITEmployeeCreateRequest:
    employee_id: int
    name: str
    dob: str
    role_title: str
    tickets_resolved: int
    projects_assigned: int
    specialization: str
    manager_ref: int
