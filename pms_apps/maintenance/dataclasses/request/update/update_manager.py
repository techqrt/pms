import dataclasses

@dataclasses.dataclass
class MaintenancePermissionUpdateRequest:
    property: bool | None = None

@dataclasses.dataclass
class MaintenanceManagerUpdateRequest:
    manager_id: int
    name: str
    dob: str
    specialization: str
    team_size: int
    years_of_experience: int
    permissions: MaintenancePermissionUpdateRequest