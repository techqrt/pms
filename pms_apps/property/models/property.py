from django.db import models
from django.contrib.postgres.fields import ArrayField
from pms_apps.authentication.models import User
from django.db.models import Q


class Property(models.Model):
    RENTAL_TYPE_CHOICES = [
        ("Residential", "Residential"),
        ("Commercial", "Commercial"),
    ]

    RENTAL_FOR_CHOICES = [
        ("Bachelor", "Bachelor"),
        ("Family", "Family"),
        ("Labour", "Labour"),
    ]

    property_id = models.AutoField(primary_key=True)
    block = models.CharField(max_length=50, null=True, blank=True)
    building_details = models.CharField(max_length=255, null=True, blank=True)
    floor = models.CharField(max_length=50, null=True, blank=True)
    flat_number = models.IntegerField(null=True, blank=True)

    dimension_length_ft = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dimension_breadth_ft = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dimension_area_sqft = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    rental_type = models.CharField(max_length=20, choices=RENTAL_TYPE_CHOICES, default="Residential")

    hall = models.BooleanField(default=False)
    bedroom_count = models.PositiveIntegerField(default=0)
    kitchen = models.BooleanField(default=False)
    attached_bathroom_count = models.PositiveIntegerField(default=0)
    single_bathroom_count = models.PositiveIntegerField(default=0)
    balcony = models.BooleanField(default=False)
    store_room = models.BooleanField(default=False)

    rental_for = models.CharField(max_length=20, choices=RENTAL_FOR_CHOICES, default="Family")

    advance_amount_rent = models.IntegerField(null=True, blank=True)
    expected_rent = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    agreement_id = models.PositiveIntegerField(null=True, blank=True)

    photos = ArrayField(models.URLField(), size=5, blank=True, null=True)
    videos = ArrayField(models.URLField(), size=5, blank=True, null=True)

    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="property_created_by"
    )
    assigned_to = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="property_assigned_to"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "property"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Property {self.property_id} - {self.building_details or 'N/A'}"


    def create(
        self,
        block: str,
        building_details: str,
        floor: str,
        flat_number: int,
        dimension_length_ft: float,
        dimension_breadth_ft: float,
        dimension_area_sqft: float,
        rental_type: str,
        hall: bool,
        bedroom_count: int,
        kitchen: bool,
        attached_bathroom_count: int,
        single_bathroom_count: int,
        balcony: bool,
        store_room: bool,
        rental_for: str,
        advance_amount_rent: int,
        expected_rent: float,
        agreement_id: int,
        photos: list[str],
        videos: list[str],
        created_by: int,
    ) -> int:
        self.block = block
        self.building_details = building_details
        self.floor = floor
        self.flat_number = flat_number
        self.dimension_length_ft = dimension_length_ft
        self.dimension_breadth_ft = dimension_breadth_ft
        self.dimension_area_sqft = dimension_area_sqft
        self.rental_type = rental_type
        self.hall = hall
        self.bedroom_count = bedroom_count
        self.kitchen = kitchen
        self.attached_bathroom_count = attached_bathroom_count
        self.single_bathroom_count = single_bathroom_count
        self.balcony = balcony
        self.store_room = store_room
        self.rental_for = rental_for
        self.advance_amount_rent = advance_amount_rent
        self.expected_rent = expected_rent
        self.agreement_id = agreement_id
        self.photos = photos
        self.videos = videos
        self.created_by_id = created_by

        self.save()
        return self.property_id


    @staticmethod
    def update(
        property_id: int,
        block: str = None,
        building_details: str = None,
        floor: str = None,
        flat_number: int = None,
        dimension_length_ft: float = None,
        dimension_breadth_ft: float = None,
        dimension_area_sqft: float = None,
        rental_type: str = None,
        hall: bool = None,
        bedroom_count: int = None,
        kitchen: bool = None,
        attached_bathroom_count: int = None,
        single_bathroom_count: int = None,
        balcony: bool = None,
        store_room: bool = None,
        rental_for: str = None,
        advance_amount_rent: int = None,
        expected_rent: float = None,
        agreement_id: int = None,
        photos: list[str] = None,
        videos: list[str] = None,
        assigned_to: int = None
    ) -> int:
        try:
            property = Property.objects.get(property_id=property_id)
        except Property.DoesNotExist:
            raise ValueError(f"Invalid Property Id: {property_id}")

        if block is not None:
            property.block = block
        if building_details is not None:
            property.building_details = building_details
        if floor is not None:
            property.floor = floor
        if flat_number is not None:
            property.flat_number = flat_number
        if dimension_length_ft is not None:
            property.dimension_length_ft = dimension_length_ft
        if dimension_breadth_ft is not None:
            property.dimension_breadth_ft = dimension_breadth_ft
        if dimension_area_sqft is not None:
            property.dimension_area_sqft = dimension_area_sqft
        if rental_type is not None:
            property.rental_type = rental_type
        if hall is not None:
            property.hall = hall
        if bedroom_count is not None:
            property.bedroom_count = bedroom_count
        if kitchen is not None:
            property.kitchen = kitchen
        if attached_bathroom_count is not None:
            property.attached_bathroom_count = attached_bathroom_count
        if single_bathroom_count is not None:
            property.single_bathroom_count = single_bathroom_count
        if balcony is not None:
            property.balcony = balcony
        if store_room is not None:
            property.store_room = store_room
        if rental_for is not None:
            property.rental_for = rental_for
        if advance_amount_rent is not None:
            property.advance_amount_rent = advance_amount_rent
        if expected_rent is not None:
            property.expected_rent = expected_rent
        if agreement_id is not None:
            property.agreement_id = agreement_id
        if photos is not None:
            property.photos = photos
        if videos is not None:
            property.videos = videos
        if assigned_to is not None:
            property.assigned_to_id = assigned_to
        
        property.save()
        return property.property_id


    @staticmethod
    def get(property_id):
        """Get property by ID."""
        return Property.objects.filter(
            property_id=property_id,
            is_active=True
        ).values(
            'property_id','block','building_details','floor','flat_number',
            'dimension_length_ft','dimension_breadth_ft','dimension_area_sqft','rental_type','hall','bedroom_count','kitchen','attached_bathroom_count','single_bathroom_count','balcony','store_room','rental_for','advance_amount_rent','expected_rent','agreement_id','photos','videos','created_by__user_id','created_by__name','created_by__phone_number','created_by__email','assigned_to__user_id','assigned_to__name','assigned_to__phone_number','assigned_to__email','created_at','updated_at','is_active'
        ).first()


    @staticmethod
    def get_all(
        sort_by: str = '',
        sort_order: str = '',
        filter_key: str = '',
        filter_value: str = '',
        search_key: str = '',
    ) -> list:
        data = Property.objects.filter(is_active=True)

        if filter_key and filter_value:
            data = data.filter(**{filter_key+"__icontains": filter_value})

        if search_key:
            data = data.filter(
                Q(building_details__icontains=search_key) |
                Q(block__icontains=search_key)
            )
        if sort_by:
            data = data.order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")
        else:
            data = data.order_by("-created_at")

        data = data.values(
            'property_id','block','building_details','floor','flat_number',
            'dimension_length_ft','dimension_breadth_ft','dimension_area_sqft','rental_type','hall','bedroom_count','kitchen','attached_bathroom_count','single_bathroom_count','balcony','store_room','rental_for','advance_amount_rent','expected_rent','agreement_id','photos','videos','created_by__user_id','created_by__name','created_by__phone_number','created_by__email','assigned_to__user_id','assigned_to__name','assigned_to__phone_number','assigned_to__email','created_at','updated_at','is_active'
        )

        return list(data)


    @staticmethod
    def delete(property_id):
        return Property.objects.filter(property_id=property_id).update(is_active=False)

    @staticmethod
    def delete_many(ids: list):
        """Soft delete multiple properties by IDs."""
        return Property.objects.filter(property_id__in=ids).update(is_active=False)
