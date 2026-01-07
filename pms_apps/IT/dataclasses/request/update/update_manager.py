import dataclasses

@dataclasses.dataclass
class ITManagerUpdateRequest:
    manager_id: int
    name: str
    dob: str
    department: str
    projects_managed: int
    systems_overseen: int
    team_size: int
