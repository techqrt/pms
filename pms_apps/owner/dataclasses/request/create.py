import dataclasses

@dataclasses.dataclass
class OwnerCreateRequest:
    owner_id: int
    name: str
    dob: str
    ownership_type: str
    properties_owned: int