import dataclasses


@dataclasses.dataclass
class MarketingEmployeeGetRequest:
    employee_id: int
    values: str