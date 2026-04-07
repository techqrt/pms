import dataclasses

@dataclasses.dataclass
class PropertyPermissionUpdateRequest:
    property : bool | None = None

@dataclasses.dataclass
class LeadUpdateRequest:
    lead_id : int
    lead_assign_to : int | None = None
    first_name : str | None = None
    last_name : str | None = None
    lead_origin : str | None = None
    address : str | None = None
    country_id : int | None = None
    city_id : int | None = None
    nationality_id : int | None = None
    passport_or_id : str | None = None
    purpose : str | None = None
    is_active : bool | None = None
    property_permission : PropertyPermissionUpdateRequest | None = None
    profile_picture : str | None = None 
