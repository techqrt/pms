import dataclasses

@dataclasses.dataclass
class ITManagerGetRequest:
    manager_id: int
    values: str
