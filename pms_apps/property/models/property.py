from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from pms_apps.authentication.models import User


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

    # -----------------------
    # CRUD Helper Functions
    # -----------------------

    @staticmethod
    def create(data):
        """Create a new property record."""
        return Property.objects.create(**data)

    @staticmethod
    def update(property_id, data):
        """Update property details by ID."""
        Property.objects.filter(property_id=property_id, is_active=True).update(**data)
        return Property.objects.filter(property_id=property_id).first()

    @staticmethod
    def get(property_id):
        """Get property by ID."""
        return Property.objects.filter(property_id=property_id, is_active=True).first()

    @staticmethod
    def get_all():
        """Get all active properties."""
        return Property.objects.filter(is_active=True).order_by("-created_at")

    @staticmethod
    def delete(property_id):
        """Soft delete property by ID."""
        return Property.objects.filter(property_id=property_id).update(is_active=False)

    @staticmethod
    def delete_many(ids: list):
        """Soft delete multiple properties by IDs."""
        return Property.objects.filter(property_id__in=ids).update(is_active=False)
