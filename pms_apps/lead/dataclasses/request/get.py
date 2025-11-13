import dataclasses

@dataclasses.dataclass
class LeadGetRequest:
    lead_id : int
    values : str