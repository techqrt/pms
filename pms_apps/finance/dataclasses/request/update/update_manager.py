import dataclasses

@dataclasses.dataclass
class FinanceManagerUpdateRequest:
    manager_id: int
    name: str
    dob: str
    department: str
    total_budget_managed: float
    reports_submitted: int
    team_size: int