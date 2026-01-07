import dataclasses

@dataclasses.dataclass
class OwnerGetRequest:
    owner_id: int
    values: str