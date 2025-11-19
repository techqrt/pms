import dataclasses

@dataclasses.dataclass
class PropertyPermissionCreateRequest:
    property : bool 

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
    property_permission : PropertyPermissionCreateRequest 