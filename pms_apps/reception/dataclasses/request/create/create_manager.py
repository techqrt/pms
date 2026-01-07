import dataclasses

@dataclasses.dataclass
class ReceptionManagerCreateRequest:
    manager_id: int
    name: str
    dob: str
    department: str
    team_size: int
    front_desk_count: int