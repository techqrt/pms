import dataclasses


@dataclasses.dataclass
class CheckInCheckOutPermissionUpdateRequest:
    lead: bool | None = None
    property: bool | None = None


@dataclasses.dataclass
class CheckInCheckOutManagerUpdateRequest:
    manager_id: int
    name: str | None = None
    dob: str | None = None
    department: str | None = None
    team_size: int | None = None
    permissions: CheckInCheckOutPermissionUpdateRequest | None = None
