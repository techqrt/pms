import dataclasses


@dataclasses.dataclass
class MarketingPermissionCreateRequest:
    lead: bool
    property: bool


@dataclasses.dataclass
class MarketingManagerCreateRequest:
    manager_id: int
    name: str
    dob: str
    department: str
    campaigns_led: int
    team_size: int
    permission: MarketingPermissionCreateRequest
