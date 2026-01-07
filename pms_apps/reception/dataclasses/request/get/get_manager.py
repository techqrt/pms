import dataclasses

@dataclasses.dataclass
class ReceptionManagerGetRequest:
    manager_id: int
    values: str