from dataclasses import dataclass
from typing import List

@dataclass
class PropertyDeleteManyRequest:
    ids: List[int]