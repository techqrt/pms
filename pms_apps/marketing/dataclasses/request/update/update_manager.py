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
    phone_number: str | None = None
    email: str | None = None
    profile_picture: str | None = None
    permissions: MarketingPermissionUpdateRequest | None = None
    old_password: str | None = None
    new_password: str | None = None