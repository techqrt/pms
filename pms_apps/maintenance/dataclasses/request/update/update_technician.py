import dataclasses
from pms_apps.maintenance.dataclasses.request.update.update_manager import MaintenancePermissionUpdateRequest

@dataclasses.dataclass
class MaintenanceTechnicianUpdateRequest:
    technician_id: int
    name: str
    dob: str
    skill_type: str
    years_of_experience: int
    assigned_jobs: int
    permissions: MaintenancePermissionUpdateRequest