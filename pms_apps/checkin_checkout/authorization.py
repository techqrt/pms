from pms_apps.checkin_checkout.models.check_in_check_out_manager import CheckInCheckOutManager
from pms_apps.checkin_checkout.models.check_in_check_out_employee import CheckInCheckOutEmployee


def get_check_in_check_out_role(user_id: int) -> str | None:
    """Returns 'Manager'/'Employee' if the user has a Check-In Check-Out profile, else None."""
    if CheckInCheckOutManager.get_id(user_id):
        return 'Manager'
    if CheckInCheckOutEmployee.objects.filter(employee_id=user_id).exists():
        return 'Employee'
    return None


def check_record_access(assigned_employee_id, user_id: int) -> None:
    """Raises ValueError if a Check-In/Check-Out Employee is not the assigned
    handler for this record. Managers and non-department users are unrestricted
    (Managers oversee the whole team; non-department access is unchanged)."""
    role = get_check_in_check_out_role(user_id)
    if role == 'Employee' and assigned_employee_id != user_id:
        raise ValueError("Not allowed to access this resource")


def resolve_parent_id(child_model, pk_field: str, pk_value, parent_field: str):
    """Looks up the parent check_in_id/check_out_id for a child record
    (document, inspection item, utility reading, payment, key) given its own
    primary key. Returns None if the child record doesn't exist."""
    if pk_value is None:
        return None
    return child_model.objects.filter(**{pk_field: pk_value}).values_list(parent_field, flat=True).first()
