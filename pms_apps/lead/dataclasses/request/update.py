import dataclasses
from pms_apps.common.sentinels import NOT_PROVIDED

@dataclasses.dataclass
class PropertyPermissionUpdateRequest:
    property : bool | None = None

@dataclasses.dataclass
class LeadUpdateRequest:
    lead_id : int
    lead_assign_to : int | None = NOT_PROVIDED
    first_name : str | None = None
    last_name : str | None = None
    lead_origin : str | None = NOT_PROVIDED
    address : str | None = NOT_PROVIDED
    country_id : int | None = NOT_PROVIDED
    city_id : int | None = NOT_PROVIDED
    nationality_id : int | None = NOT_PROVIDED
    passport_or_id : str | None = NOT_PROVIDED
    purpose : str | None = None
    po_box : str | None = NOT_PROVIDED
    feedback : str | None = NOT_PROVIDED
    lead_category : str | None = NOT_PROVIDED
    is_active : bool | None = None
    property_permission : PropertyPermissionUpdateRequest | None = None
    email : str | None = NOT_PROVIDED
    profile_picture : str | None = NOT_PROVIDED
    civil_id : str | None = NOT_PROVIDED
    estimated_closing_date : str | None = NOT_PROVIDED
    phone_number : str | None = NOT_PROVIDED
    tenant_code : str | None = NOT_PROVIDED
