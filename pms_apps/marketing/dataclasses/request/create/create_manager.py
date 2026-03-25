import dataclasses
from pms_apps.common.dataclasses.request.permission import Permissions


@dataclasses.dataclass
class MarketingManagerCreateRequest:
    manager_id: int
    name: str
    dob: str
    department: str
    campaigns_led: int
    team_size: int
    permissions: Permissions
    profile_picture: str | None = None
