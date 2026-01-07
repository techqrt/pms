import dataclasses

@dataclasses.dataclass
class CollectionEmployeeGetRequest:
    employeeq_id: int
    values: str