import dataclasses

@dataclasses.dataclass
class CollectionManagerUpdateRequest:
    manager_id: int
    name: str
    dob: str
    department: str
    total_collections: float
    overdue_accounts_managed: int
    team_size: int