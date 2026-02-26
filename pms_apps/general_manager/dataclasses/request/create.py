import dataclasses

@dataclasses.dataclass
class GeneralManagerCreateRequest:
    general_manager_id: int
    name: str
    dob: str
    department: str
    years_of_experience: int