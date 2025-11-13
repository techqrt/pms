from dataclasses import dataclass
from typing import Optional

@dataclass
class PropertyGetRequest:
    property_id: Optional[int] = None