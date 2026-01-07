import dataclasses

@dataclasses.dataclass
class LegalManagerGetRequest:
    manager_id: int
    values: str
