from dataclasses import dataclass

@dataclass
class PermissionsProperty:
    property: bool

@dataclass
class PermissionsLead:
    lead: bool

@dataclass
class PermissionsMarketing:
    marketing : bool

@dataclass
class PermissionMaintenance:
    maintenance : bool

@dataclass
class PermissionReception:
    reception : bool

@dataclass
class PermissionFinance:
    finance : bool

@dataclass
class PermissionCollection:
    collection : bool

@dataclass
class PermissionLegal:
    legal : bool

@dataclass
class PermissionIT:
    it : bool

@dataclass
class PermissionGeneralManager:
    general_manager : bool

@dataclass
class PermissionHR:
    hr : bool

@dataclass
class PermissionOwner:
    owner : bool


@dataclass
class Permissions:
    property: PermissionsProperty | None = None
    lead : PermissionsLead | None = None
    marketing : PermissionsMarketing | None = None
    maintenance : PermissionMaintenance | None = None
    reception : PermissionReception | None = None
    finance : PermissionFinance | None = None
    collection : PermissionCollection | None = None
    legal : PermissionLegal | None = None
    it : PermissionIT | None = None
    general_manager : PermissionGeneralManager | None = None
    hr : PermissionHR | None = None
    owner : PermissionOwner | None = None
    