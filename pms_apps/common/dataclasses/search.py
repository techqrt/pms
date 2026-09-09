from dataclasses import dataclass

from pms.config import Configurations


@dataclass
class Search:
    key: str
    page_num: int
    limit: int

    def __post_init__(self):
        self.limit = min(self.limit, Configurations.max_pagination_limit)
