import dataclasses
from pms_apps.maintenance.dataclasses.request.update.update_manager import MaintenancePermissionUpdateRequest

@dataclasses.dataclass
class MaintenanceEmployeeUpdateRequest:
    employee_id: int
    name: str
    dob: str
    designation: str
    specialization: str
    assigned_tasks: int
    manager_ref: int
    permissions: MaintenancePermissionUpdateRequest