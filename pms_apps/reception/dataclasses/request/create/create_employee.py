import dataclasses

@dataclasses.dataclass
class ReceptionEmployeeCreateRequest:
    employee_id: int
    name: str
    dob: str
    shift: str
    desk_number: str
    calls_handled: int
    visitors_logged: int
    manager_ref: int