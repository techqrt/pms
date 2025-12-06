import dataclasses
from pms_apps.marketing.dataclasses.request.create.create_manager import MarketingPermissionCreateRequest


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
    permission: MarketingPermissionCreateRequest
