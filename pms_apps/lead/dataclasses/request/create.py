import dataclasses
from pms_apps.common.dataclasses.request.permission import Permissions


@dataclasses.dataclass
class LeadCreateRequest:
    lead_assign_to : int
    first_name : str 
    last_name : str
    lead_origin : str
    address : str
    nationality : int
    passport_or_id : str
    purpose : str
    permissions : Permissions