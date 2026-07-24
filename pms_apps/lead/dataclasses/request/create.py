import dataclasses
from pms_apps.common.dataclasses.request.permission import Permissions


@dataclasses.dataclass
class LeadCreateRequest:
    lead_assign_to : int
    first_name : str 
    last_name : str
    phone_number : str
    lead_origin : str
    address : str
    country_id : int
    city_id : int
    nationality_id : int
    purpose : str
    permissions : Permissions
    passport_or_id : str | None = None
    po_box : str | None = None
    feedback : str | None = None
    lead_category : str | None = None
    profile_picture : str | None = None
    civil_id : str | None = None
    estimated_closing_date : str | None = None
