import dataclasses

@dataclasses.dataclass
class ITManagerCreateRequest:
    manager_id: int
    name: str
    dob: str
    department: str
    projects_managed: int
    systems_overseen: int
    team_size: int
