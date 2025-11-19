from dataclasses import dataclass
from typing import List

@dataclass
class PropertyDeleteManyRequest:
    property_ids: List[int]