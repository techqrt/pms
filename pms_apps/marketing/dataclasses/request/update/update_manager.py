import dataclasses

@dataclasses.dataclass
class MarketingPermissionUpdateRequest:
    lead: bool | None = None
    property: bool | None = None

@dataclasses.dataclass
class MarketingManagerUpdateRequest:
    manager_id: int
    name: str
    dob: str
    department: str
    campaigns_led: int
    team_size: int
    permission: MarketingPermissionUpdateRequest