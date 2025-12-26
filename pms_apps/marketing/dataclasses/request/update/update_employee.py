import dataclasses
from pms_apps.marketing.dataclasses.request.update.update_manager import MarketingPermissionUpdateRequest

@dataclasses.dataclass
class MarketingEmployeeUpdateRequest:
    employee_id: int
    name: str
    dob: str
    designation: str
    department: str
    campaigns_assigned: int
    leads_generated: int
    manager_ref: int
    permissions: MarketingPermissionUpdateRequest