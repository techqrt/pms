from django.db import models
from django.db.models import Q


class Building(models.Model):
    building_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=255)
    block = models.CharField(max_length=50, null=True, blank=True)
    total_floors = models.PositiveIntegerField(null=True, blank=True)
    year_of_construction = models.PositiveIntegerField(null=True, blank=True)

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
        address_line_1: str,
        area_zone: str,
        city: str,
        state: str,
        country: str,
        pincode: str,
        block: str = None,
        total_floors: int = None,
        year_of_construction: int = None,
        address_line_2: str = None,
        google_map_location: str = None,
        internal_notes: str = None,
        created_by: int = None,
    ) -> int:
        self.name = name
        self.block = block
        self.total_floors = total_floors
        self.year_of_construction = year_of_construction
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.area_zone = area_zone
        self.city = city
        self.state = state
        self.country = country
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
        block: str = None,
        total_floors: int = None,
        year_of_construction: int = None,
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
        if block is not None:
            building.block = block
        if total_floors is not None:
            building.total_floors = total_floors
        if year_of_construction is not None:
            building.year_of_construction = year_of_construction
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
            building.country = country
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
            'building_id', 'name', 'block', 'total_floors', 'year_of_construction',
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
            'building_id', 'name', 'block', 'total_floors', 'year_of_construction',
            'address_line_1', 'address_line_2', 'area_zone', 'city', 'state', 'country',
            'pincode', 'google_map_location', 'internal_notes',
            'created_by__user_id', 'created_by__name',
            'created_at', 'updated_at', 'is_active'
        ))

    @staticmethod
    def delete(building_id: int):
        return Building.objects.filter(building_id=building_id).update(is_active=False)
