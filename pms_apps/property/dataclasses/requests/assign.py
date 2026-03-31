from dataclasses import dataclass

@dataclass
class PropertyAssignRequest:
    property_id: int
    tenant_id: int
