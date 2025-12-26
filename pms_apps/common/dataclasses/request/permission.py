from dataclasses import dataclass

@dataclass
class PermissionsProperty:
    property: bool

@dataclass
class PermissionsLead:
    lead: bool


@dataclass
class Permissions:
    property: PermissionsProperty
    lead : PermissionsLead