import dataclasses

@dataclasses.dataclass
class GeneralManagerGetRequest:
    generalmanager_id: int
    values: str