import dataclasses
from pms_apps.common.dataclasses.request.permission import Permissions

@dataclasses.dataclass
class MaintenanceManagerCreateRequest:
    manager_id: int
    name: str
    dob: str
    specialization: str
    team_size: int
    years_of_experience: int
    permissions: Permissions