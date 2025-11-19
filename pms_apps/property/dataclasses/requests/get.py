from dataclasses import dataclass

@dataclass
class PropertyGetRequest:
    property_id : int
    values : str