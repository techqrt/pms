import dataclasses
from pms_apps.common.dataclasses.request.permission import Permissions


@dataclasses.dataclass
class LeadCreateRequest:
    lead_assign_to : int | None
    first_name : str
    last_name : str
    phone_number : str
    address : str | None
    country_id : int | None
    city_id : int | None
    purpose : str
    permissions : Permissions
    lead_origin : str | None = None
    nationality_id : int | None = None
    passport_or_id : str | None = None
    po_box : str | None = None
    feedback : str | None = None
    lead_category : str | None = None
    profile_picture : str | None = None
    civil_id : str | None = None
    estimated_closing_date : str | None = None
