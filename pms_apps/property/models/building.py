from django.db import models
from django.db.models import Q


class Building(models.Model):
    RENTAL_PURPOSE_CHOICES = [
        ("Residential", "Residential"),
        ("Commercial", "Commercial"),
    ]

    # Mirrors property.Property.RENTAL_TYPE_CHOICES. A Building's property_type
    # locks which unit rental_type may be created/moved into it (see
    # PropertyView.create_extract/update_extract). Nullable only to grandfather
    # pre-existing buildings backfilled from ambiguous/mixed-type legacy data.
    PROPERTY_TYPE_CHOICES = [
        ("Flat", "Flat"),
        ("Commercial", "Commercial"),
        ("Villa", "Villa"),
        ("Warehouse", "Warehouse"),
    ]

    # Mirror the exact choices used by the matching Property type-specific
    # serializer/model fields, so a value entered here means the same thing
    # as its per-unit counterpart.
    COMMERCIAL_CATEGORY_CHOICES = [
        ("Shop", "Shop"),
        ("Office", "Office"),
        ("Showroom", "Showroom"),
        ("Godown", "Godown"),
        ("Industrial Unit", "Industrial Unit"),
    ]
    LIFT_TYPE_CHOICES = [
        ("Passenger", "Passenger"),
        ("Goods", "Goods"),
        ("Both", "Both"),
    ]
    PARKING_AVAILABILITY_CHOICES = [
        ("Open", "Open"),
        ("Covered", "Covered"),
        ("Both", "Both"),
    ]
    WAREHOUSE_CATEGORY_CHOICES = [
        ("Industrial Warehouse", "Industrial Warehouse"),
        ("Logistics Warehouse", "Logistics Warehouse"),
        ("Cold Storage", "Cold Storage"),
        ("Godown", "Godown"),
    ]
    OWNERSHIP_TYPE_CHOICES = [
        ("Owned", "Owned"),
        ("Leased", "Leased"),
    ]
    WATER_SUPPLY_SOURCE_CHOICES = [
        ("Borewell", "Borewell"),
        ("Municipal", "Municipal"),
        ("Tanker", "Tanker"),
    ]
    PRIVATE_PARKING_CHOICES = [
        ("Open", "Open"),
        ("Covered", "Covered"),
        ("Both", "Both"),
    ]
    SWIMMING_POOL_CHOICES = [
        ("No", "No"),
        ("Private", "Private"),
        ("Common", "Common"),
    ]

    building_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=255)
    property_type = models.CharField(
        max_length=20, choices=PROPERTY_TYPE_CHOICES, null=True, blank=True
    )
    block = models.CharField(max_length=50, null=True, blank=True)
    total_floors = models.PositiveIntegerField(null=True, blank=True)
    year_of_construction = models.PositiveIntegerField(null=True, blank=True)

    # Building-level common facilities/amenities, e.g. ["Parking", "Lift", "CCTV"]
    facilities = models.JSONField(default=list, blank=True)
    # Building-level tenant preference
    rental_purpose = models.CharField(
        max_length=20, choices=RENTAL_PURPOSE_CHOICES, null=True, blank=True
    )
    allowed_tenant_types = models.JSONField(default=list, blank=True)

    # Flat-specific structured amenities (only meaningful when property_type == "Flat")
    parking = models.BooleanField(default=False, null=True)
    lift = models.BooleanField(default=False, null=True)
    security = models.BooleanField(default=False, null=True)
    gas_pipeline = models.BooleanField(default=False, null=True)
    water_supply = models.BooleanField(default=False, null=True)
    intercom = models.BooleanField(default=False, null=True)
    fire_safety = models.BooleanField(default=False, null=True)

    # Villa-specific (only meaningful when property_type == "Villa")
    project_name = models.CharField(max_length=150, null=True, blank=True)
    private_garden = models.BooleanField(default=False, null=True)
    private_parking = models.CharField(
        max_length=10, choices=PRIVATE_PARKING_CHOICES, null=True, blank=True
    )
    swimming_pool = models.CharField(
        max_length=10, choices=SWIMMING_POOL_CHOICES, null=True, blank=True
    )
    terrace_access = models.BooleanField(default=False, null=True)
    boundary_wall = models.BooleanField(default=False, null=True)
    driveway = models.BooleanField(default=False, null=True)
    water_supply_24x7 = models.BooleanField(default=False, null=True)
    security_guard = models.BooleanField(default=False, null=True)
    clubhouse_access = models.BooleanField(default=False, null=True)
    gym = models.BooleanField(default=False, null=True)
    childrens_play_area = models.BooleanField(default=False, null=True)
    internal_roads = models.BooleanField(default=False, null=True)
    street_lights = models.BooleanField(default=False, null=True)
    gated_community = models.BooleanField(default=False, null=True)

    # Shared between Flat and Villa
    power_backup = models.BooleanField(default=False, null=True)

    # Commercial-specific (only meaningful when property_type == "Commercial")
    commercial_category = models.CharField(
        max_length=30, choices=COMMERCIAL_CATEGORY_CHOICES, null=True, blank=True
    )
    lift_type = models.CharField(max_length=20, choices=LIFT_TYPE_CHOICES, null=True, blank=True)
    fire_safety_compliant = models.BooleanField(default=False, null=True)
    emergency_exit = models.BooleanField(default=False, null=True)
    parking_availability = models.CharField(
        max_length=20, choices=PARKING_AVAILABILITY_CHOICES, null=True, blank=True
    )
    cctv = models.BooleanField(default=False, null=True)

    # Warehouse-specific (only meaningful when property_type == "Warehouse")
    warehouse_category = models.CharField(
        max_length=30, choices=WAREHOUSE_CATEGORY_CHOICES, null=True, blank=True
    )
    industrial_estate_name = models.CharField(max_length=150, null=True, blank=True)
    ownership_type = models.CharField(
        max_length=20, choices=OWNERSHIP_TYPE_CHOICES, null=True, blank=True
    )
    has_transformer = models.BooleanField(default=False, null=True)
    water_supply_source = models.CharField(
        max_length=20, choices=WATER_SUPPLY_SOURCE_CHOICES, null=True, blank=True
    )
    has_drainage_system = models.BooleanField(default=False, null=True)
    has_internet_fiber = models.BooleanField(default=False, null=True)
    allowed_industry_types = models.JSONField(default=list, blank=True)

    # Shared between Commercial and Warehouse
    power_load_kw = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    has_dg_backup = models.BooleanField(default=False, null=True)

    address_line_1 = models.TextField()
    address_line_2 = models.TextField(null=True, blank=True)
    area_zone = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    google_map_location = models.TextField(null=True, blank=True)

    internal_notes = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(
        "authentication.User", on_delete=models.DO_NOTHING, null=True, blank=True,
        related_name="buildings_created"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "building"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Building {self.building_id} - {self.name}"

    def create(
        self,
        name: str,
        property_type: str,
        address_line_1: str,
        area_zone: str,
        city: str,
        state: str,
        country: str,
        pincode: str,
        block: str = None,
        total_floors: int = None,
        year_of_construction: int = None,
        facilities: list = None,
        rental_purpose: str = None,
        allowed_tenant_types: list = None,
        parking: bool = None,
        lift: bool = None,
        security: bool = None,
        gas_pipeline: bool = None,
        water_supply: bool = None,
        intercom: bool = None,
        fire_safety: bool = None,
        project_name: str = None,
        private_garden: bool = None,
        private_parking: str = None,
        swimming_pool: str = None,
        terrace_access: bool = None,
        boundary_wall: bool = None,
        driveway: bool = None,
        water_supply_24x7: bool = None,
        security_guard: bool = None,
        clubhouse_access: bool = None,
        gym: bool = None,
        childrens_play_area: bool = None,
        internal_roads: bool = None,
        street_lights: bool = None,
        gated_community: bool = None,
        power_backup: bool = None,
        commercial_category: str = None,
        lift_type: str = None,
        fire_safety_compliant: bool = None,
        emergency_exit: bool = None,
        parking_availability: str = None,
        cctv: bool = None,
        warehouse_category: str = None,
        industrial_estate_name: str = None,
        ownership_type: str = None,
        has_transformer: bool = None,
        water_supply_source: str = None,
        has_drainage_system: bool = None,
        has_internet_fiber: bool = None,
        allowed_industry_types: list = None,
        power_load_kw: float = None,
        has_dg_backup: bool = None,
        address_line_2: str = None,
        google_map_location: str = None,
        internal_notes: str = None,
        created_by: int = None,
    ) -> int:
        self.name = name
        self.property_type = property_type
        self.block = block
        self.total_floors = total_floors
        self.year_of_construction = year_of_construction
        self.facilities = facilities or []
        self.rental_purpose = rental_purpose
        self.allowed_tenant_types = allowed_tenant_types or []
        self.parking = parking
        self.lift = lift
        self.security = security
        self.gas_pipeline = gas_pipeline
        self.water_supply = water_supply
        self.intercom = intercom
        self.fire_safety = fire_safety
        self.project_name = project_name
        self.private_garden = private_garden
        self.private_parking = private_parking
        self.swimming_pool = swimming_pool
        self.terrace_access = terrace_access
        self.boundary_wall = boundary_wall
        self.driveway = driveway
        self.water_supply_24x7 = water_supply_24x7
        self.security_guard = security_guard
        self.clubhouse_access = clubhouse_access
        self.gym = gym
        self.childrens_play_area = childrens_play_area
        self.internal_roads = internal_roads
        self.street_lights = street_lights
        self.gated_community = gated_community
        self.power_backup = power_backup
        self.commercial_category = commercial_category
        self.lift_type = lift_type
        self.fire_safety_compliant = fire_safety_compliant
        self.emergency_exit = emergency_exit
        self.parking_availability = parking_availability
        self.cctv = cctv
        self.warehouse_category = warehouse_category
        self.industrial_estate_name = industrial_estate_name
        self.ownership_type = ownership_type
        self.has_transformer = has_transformer
        self.water_supply_source = water_supply_source
        self.has_drainage_system = has_drainage_system
        self.has_internet_fiber = has_internet_fiber
        self.allowed_industry_types = allowed_industry_types or []
        self.power_load_kw = power_load_kw
        self.has_dg_backup = has_dg_backup
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.area_zone = area_zone
        self.city = city
        self.state = state
        self.country = country.strip().title() if country else country
        self.pincode = pincode
        self.google_map_location = google_map_location
        self.internal_notes = internal_notes
        self.created_by_id = created_by

        self.save()
        return self.building_id

    @staticmethod
    def update(
        building_id: int,
        name: str = None,
        property_type: str = None,
        block: str = None,
        total_floors: int = None,
        year_of_construction: int = None,
        facilities: list = None,
        rental_purpose: str = None,
        allowed_tenant_types: list = None,
        parking: bool = None,
        lift: bool = None,
        security: bool = None,
        gas_pipeline: bool = None,
        water_supply: bool = None,
        intercom: bool = None,
        fire_safety: bool = None,
        project_name: str = None,
        private_garden: bool = None,
        private_parking: str = None,
        swimming_pool: str = None,
        terrace_access: bool = None,
        boundary_wall: bool = None,
        driveway: bool = None,
        water_supply_24x7: bool = None,
        security_guard: bool = None,
        clubhouse_access: bool = None,
        gym: bool = None,
        childrens_play_area: bool = None,
        internal_roads: bool = None,
        street_lights: bool = None,
        gated_community: bool = None,
        power_backup: bool = None,
        commercial_category: str = None,
        lift_type: str = None,
        fire_safety_compliant: bool = None,
        emergency_exit: bool = None,
        parking_availability: str = None,
        cctv: bool = None,
        warehouse_category: str = None,
        industrial_estate_name: str = None,
        ownership_type: str = None,
        has_transformer: bool = None,
        water_supply_source: str = None,
        has_drainage_system: bool = None,
        has_internet_fiber: bool = None,
        allowed_industry_types: list = None,
        power_load_kw: float = None,
        has_dg_backup: bool = None,
        address_line_1: str = None,
        address_line_2: str = None,
        area_zone: str = None,
        city: str = None,
        state: str = None,
        country: str = None,
        pincode: str = None,
        google_map_location: str = None,
        internal_notes: str = None,
    ) -> int:
        try:
            building = Building.objects.get(building_id=building_id)
        except Building.DoesNotExist:
            raise ValueError(f"Invalid Building Id: {building_id}")

        if name is not None:
            building.name = name
        if property_type is not None:
            building.property_type = property_type
        if block is not None:
            building.block = block
        if total_floors is not None:
            building.total_floors = total_floors
        if year_of_construction is not None:
            building.year_of_construction = year_of_construction
        if facilities is not None:
            building.facilities = facilities
        if rental_purpose is not None:
            building.rental_purpose = rental_purpose
        if allowed_tenant_types is not None:
            building.allowed_tenant_types = allowed_tenant_types
        if parking is not None:
            building.parking = parking
        if lift is not None:
            building.lift = lift
        if security is not None:
            building.security = security
        if gas_pipeline is not None:
            building.gas_pipeline = gas_pipeline
        if water_supply is not None:
            building.water_supply = water_supply
        if intercom is not None:
            building.intercom = intercom
        if fire_safety is not None:
            building.fire_safety = fire_safety
        if project_name is not None:
            building.project_name = project_name
        if private_garden is not None:
            building.private_garden = private_garden
        if private_parking is not None:
            building.private_parking = private_parking
        if swimming_pool is not None:
            building.swimming_pool = swimming_pool
        if terrace_access is not None:
            building.terrace_access = terrace_access
        if boundary_wall is not None:
            building.boundary_wall = boundary_wall
        if driveway is not None:
            building.driveway = driveway
        if water_supply_24x7 is not None:
            building.water_supply_24x7 = water_supply_24x7
        if security_guard is not None:
            building.security_guard = security_guard
        if clubhouse_access is not None:
            building.clubhouse_access = clubhouse_access
        if gym is not None:
            building.gym = gym
        if childrens_play_area is not None:
            building.childrens_play_area = childrens_play_area
        if internal_roads is not None:
            building.internal_roads = internal_roads
        if street_lights is not None:
            building.street_lights = street_lights
        if gated_community is not None:
            building.gated_community = gated_community
        if power_backup is not None:
            building.power_backup = power_backup
        if commercial_category is not None:
            building.commercial_category = commercial_category
        if lift_type is not None:
            building.lift_type = lift_type
        if fire_safety_compliant is not None:
            building.fire_safety_compliant = fire_safety_compliant
        if emergency_exit is not None:
            building.emergency_exit = emergency_exit
        if parking_availability is not None:
            building.parking_availability = parking_availability
        if cctv is not None:
            building.cctv = cctv
        if warehouse_category is not None:
            building.warehouse_category = warehouse_category
        if industrial_estate_name is not None:
            building.industrial_estate_name = industrial_estate_name
        if ownership_type is not None:
            building.ownership_type = ownership_type
        if has_transformer is not None:
            building.has_transformer = has_transformer
        if water_supply_source is not None:
            building.water_supply_source = water_supply_source
        if has_drainage_system is not None:
            building.has_drainage_system = has_drainage_system
        if has_internet_fiber is not None:
            building.has_internet_fiber = has_internet_fiber
        if allowed_industry_types is not None:
            building.allowed_industry_types = allowed_industry_types
        if power_load_kw is not None:
            building.power_load_kw = power_load_kw
        if has_dg_backup is not None:
            building.has_dg_backup = has_dg_backup
        if address_line_1 is not None:
            building.address_line_1 = address_line_1
        if address_line_2 is not None:
            building.address_line_2 = address_line_2
        if area_zone is not None:
            building.area_zone = area_zone
        if city is not None:
            building.city = city
        if state is not None:
            building.state = state
        if country is not None:
            building.country = country.strip().title()
        if pincode is not None:
            building.pincode = pincode
        if google_map_location is not None:
            building.google_map_location = google_map_location
        if internal_notes is not None:
            building.internal_notes = internal_notes

        building.save()
        return building.building_id

    @staticmethod
    def get(building_id: int):
        """Get building by ID."""
        return Building.objects.filter(
            building_id=building_id,
            is_active=True
        ).values(
            'building_id', 'name', 'property_type', 'block', 'total_floors', 'year_of_construction',
            'facilities', 'rental_purpose', 'allowed_tenant_types',
            'parking', 'lift', 'security', 'gas_pipeline', 'water_supply', 'intercom', 'fire_safety',
            'project_name', 'private_garden', 'private_parking', 'swimming_pool', 'terrace_access',
            'boundary_wall', 'driveway', 'water_supply_24x7', 'security_guard', 'clubhouse_access',
            'gym', 'childrens_play_area', 'internal_roads', 'street_lights', 'gated_community',
            'power_backup',
            'commercial_category', 'lift_type', 'fire_safety_compliant', 'emergency_exit',
            'parking_availability', 'cctv',
            'warehouse_category', 'industrial_estate_name', 'ownership_type', 'has_transformer',
            'water_supply_source', 'has_drainage_system', 'has_internet_fiber', 'allowed_industry_types',
            'power_load_kw', 'has_dg_backup',
            'address_line_1', 'address_line_2', 'area_zone', 'city', 'state', 'country',
            'pincode', 'google_map_location', 'internal_notes',
            'created_by__user_id', 'created_by__name',
            'created_at', 'updated_at', 'is_active'
        ).first()

    @staticmethod
    def get_all(search_key: str = '') -> list:
        data = Building.objects.filter(is_active=True)

        if search_key:
            data = data.filter(
                Q(name__icontains=search_key) |
                Q(city__icontains=search_key) |
                Q(block__icontains=search_key)
            )

        data = data.order_by("-created_at")

        return list(data.values(
            'building_id', 'name', 'property_type', 'block', 'total_floors', 'year_of_construction',
            'facilities', 'rental_purpose', 'allowed_tenant_types',
            'parking', 'lift', 'security', 'gas_pipeline', 'water_supply', 'intercom', 'fire_safety',
            'project_name', 'private_garden', 'private_parking', 'swimming_pool', 'terrace_access',
            'boundary_wall', 'driveway', 'water_supply_24x7', 'security_guard', 'clubhouse_access',
            'gym', 'childrens_play_area', 'internal_roads', 'street_lights', 'gated_community',
            'power_backup',
            'commercial_category', 'lift_type', 'fire_safety_compliant', 'emergency_exit',
            'parking_availability', 'cctv',
            'warehouse_category', 'industrial_estate_name', 'ownership_type', 'has_transformer',
            'water_supply_source', 'has_drainage_system', 'has_internet_fiber', 'allowed_industry_types',
            'power_load_kw', 'has_dg_backup',
            'address_line_1', 'address_line_2', 'area_zone', 'city', 'state', 'country',
            'pincode', 'google_map_location', 'internal_notes',
            'created_by__user_id', 'created_by__name',
            'created_at', 'updated_at', 'is_active'
        ))

    @staticmethod
    def delete(building_id: int):
        return Building.objects.filter(building_id=building_id).update(is_active=False)
