import dataclasses


@dataclasses.dataclass
class ITEmployeeDeleteRequest:
    employee_id: int
