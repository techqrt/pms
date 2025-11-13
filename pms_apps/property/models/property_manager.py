from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User


class PropertyManager(models.Model):
    manager_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="property_manager_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    region = models.CharField(max_length=100, blank=True, null=True)           # e.g., North Zone, South Zone
    properties_managed = models.IntegerField(default=0)
    team_size = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "property_manager"

    def __str__(self):
        return f"{self.name} ({self.manager_id.phone_number})"

    # ----------------------
    # CRUD Operations
    # ----------------------

    def create(
        self,
        manager_id: int,
        name: str,
        dob=None,
        region: str = "",
        properties_managed: int = 0,
        team_size: int = 0,
    ) -> int:
        """Create new Property Manager"""
        self.manager_id_id = manager_id
        self.name = name
        self.dob = dob
        self.region = region
        self.properties_managed = properties_managed
        self.team_size = team_size
        self.created_date_time = timezone.now()
        self.save()
        return self.manager_id_id

    @staticmethod
    def update(
        manager_id: int,
        name: str,
        dob=None,
        region: str = "",
        properties_managed: int = 0,
        team_size: int = 0,
    ) -> int:
        """Update Property Manager"""
        m = PropertyManager.objects.get(manager_id=manager_id)
        m.name = name
        m.dob = dob
        m.region = region
        m.properties_managed = properties_managed
        m.team_size = team_size
        m.save()
        return m.manager_id_id

    @staticmethod
    def remove(manager_id: int) -> None:
        """Delete Property Manager"""
        PropertyManager.objects.get(manager_id=manager_id).delete()

    @staticmethod
    def get(manager_id: int) -> dict:
        """Fetch single Property Manager"""
        return PropertyManager.objects.filter(manager_id=manager_id).values(
            "manager_id",
            "name",
            "dob",
            "region",
            "properties_managed",
            "team_size",
            "created_date_time",
            "manager_id__phone_number",
            "manager_id__email",
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all Property Managers"""
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            PropertyManager.objects.filter(filters).values(
                "manager_id",
                "name",
                "dob",
                "region",
                "properties_managed",
                "team_size",
                "created_date_time",
                "manager_id__phone_number",
                "manager_id__email",
            )
        )


