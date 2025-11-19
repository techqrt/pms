from dataclasses import dataclass
from typing import Optional, List


@dataclass
class PropertyUserRequest:
    user_id: Optional[int] = None
    name: Optional[str] = None
    role: Optional[str] = None            # "Marketing Manager", "Marketing Employee", or "Other"
    department: Optional[str] = None      # Only used if Marketing Manager