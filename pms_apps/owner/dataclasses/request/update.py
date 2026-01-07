import dataclasses


@dataclasses.dataclass
class OwnerUpdateRequest:
    owner_id: int
    name: str
    dob: str
    ownership_type: str
    properties_owned: int
