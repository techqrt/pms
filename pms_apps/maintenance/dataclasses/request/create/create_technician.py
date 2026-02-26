import dataclasses
from pms_apps.common.dataclasses.request.permission import Permissions

@dataclasses.dataclass
class MaintenanceTechnicianCreateRequest:
    technician_id: int
    name: str
    dob: str
    skill_type: str
    years_of_experience: int
    assigned_jobs: int
    permissions: Permissions