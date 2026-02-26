import dataclasses

@dataclasses.dataclass
class FinanceEmployeeGetRequest:
    employee_id: int
    values: str