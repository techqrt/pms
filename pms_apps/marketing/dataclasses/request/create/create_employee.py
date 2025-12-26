import dataclasses
from pms_apps.common.dataclasses.request.permission import Permissions


@dataclasses.dataclass
class MarketingEmployeeCreateRequest:
    employee_id: int
    name: str
    dob: str
    designation: str
    department: str
    campaigns_assigned: int
    leads_generated: int
    manager_ref: int
    permissions: Permissions
