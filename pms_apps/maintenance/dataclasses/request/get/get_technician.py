import dataclasses

@dataclasses.dataclass
class MaintenanceTechnicianGetRequest:
    technician_id: int
    values: str