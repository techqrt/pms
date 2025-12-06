import dataclasses

@dataclasses.dataclass
class MaintenanceManagerGetRequest:
    manager_id: int
    values: str