import dataclasses

@dataclasses.dataclass
class CollectionManagerGetRequest:
    manager_id: int
    values: str