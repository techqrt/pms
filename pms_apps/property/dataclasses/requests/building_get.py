from dataclasses import dataclass


@dataclass
class BuildingGetRequest:
    building_id: int
    values: str
