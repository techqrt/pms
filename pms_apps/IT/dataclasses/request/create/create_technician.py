import dataclasses

@dataclasses.dataclass
class ITTechnicianCreateRequest:
    technician_id: int
    name: str
    dob: str
    skill_area: str
    tickets_closed: int
    years_of_experience: int
