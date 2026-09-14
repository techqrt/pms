import dataclasses

from pms_apps.checkin_checkout.dataclasses.requests.update_manager import CheckInCheckOutPermissionUpdateRequest


@dataclasses.dataclass
class CheckInCheckOutEmployeeUpdateRequest:
    employee_id: int
    name: str | None = None
    dob: str | None = None
    designation: str | None = None
    department: str | None = None
    manager_ref: int | None = None
    permissions: CheckInCheckOutPermissionUpdateRequest | None = None
