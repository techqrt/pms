import dataclasses


@dataclasses.dataclass
class MarketingManagerGetRequest:
    manager_id: int
    values: str