from dataclasses import dataclass

@dataclass
class PermissionsProperty:
    property: bool


@dataclass
class Permissions:
    property: PermissionsProperty