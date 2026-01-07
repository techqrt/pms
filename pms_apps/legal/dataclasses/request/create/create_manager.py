import dataclasses

@dataclasses.dataclass
class LegalManagerCreateRequest:
    manager_id: int
    name: str
    dob: str
    department: str
    total_cases_handled: int
    open_cases: int
    closed_cases: int
    team_size: int
