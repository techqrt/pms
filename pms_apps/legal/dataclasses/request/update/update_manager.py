import dataclasses

@dataclasses.dataclass
class LegalManagerUpdateRequest:
    manager_id: int
    name: str
    dob: str
    department: str
    total_cases_handled: int
    open_cases: int
    closed_cases: int
    team_size: int
