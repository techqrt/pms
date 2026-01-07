import dataclasses

@dataclasses.dataclass
class FinanceManagerGetRequest:
    manager_id: int
    values: str