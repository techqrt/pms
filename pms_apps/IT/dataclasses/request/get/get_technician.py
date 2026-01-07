import dataclasses

@dataclasses.dataclass
class ITTechnicianGetRequest:
    technician_id: int
    values: str
