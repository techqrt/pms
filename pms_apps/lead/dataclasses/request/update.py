import dataclasses

@dataclasses.dataclass
class LeadUpdateRequest:
    lead_id : int
    lead_assign_to : int 
    first_name : str 
    last_name : str 
    lead_origin : str 
    address : str 
    nationality : int 
    passport_or_id : str 
    purpose : str 
