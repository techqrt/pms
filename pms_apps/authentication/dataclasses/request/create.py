from dataclasses import dataclass
from typing import Optional, List


@dataclass
class PropertyUserRequest:
    """
    Represents a user reference — can be either a MarketingEmployee or MarketingManager.
    This keeps the Property dataclasses flexible and clean.
    """
    user_id: Optional[int] = None
    name: Optional[str] = None
    role: Optional[str] = None            # "Marketing Manager", "Marketing Employee", or "Other"
    department: Optional[str] = None      # Only used if Marketing Manager