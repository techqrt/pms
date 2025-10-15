from django.db import models
from django.utils import timezone
from pms_apps.authentication.models import User


class StoreManager(models.Model):
    # Link directly with User (each user can have one Store Manager profile)
    storemanager_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="storemanager_profile")

    # Extra fields specific to Store Manager
    name = models.CharField(max_length=100, default='')
    dob = models.DateField(null=True, blank=True)
    store_name = models.CharField(max_length=150, blank=True, null=True)       # Store they manage
    location = models.CharField(max_length=200, blank=True, null=True)         # Store location
    employees_managed = models.IntegerField(default=0)                         # Number of employees managed

    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "store_manager"

    def __str__(self):
        return f"{self.name} ({self.storemanager_id.username})"

    # ----------------------
    # Static CRUD Operations
    # ----------------------

    def create(self, storemanager_id: int, name: str, dob=None, store_name: str = "", location: str = "", employees_managed: int = 0) -> int:
        """Create a new Store Manager profile"""
        self.storemanager_id_id = storemanager_id
        self.name = name
        self.dob = dob
        self.store_name = store_name
        self.location = location
        self.employees_managed = employees_managed
        self.created_date_time = timezone.now()
        self.save()
        return self.storemanager_id_id

    @staticmethod
    def update(storemanager_id: int, name: str, dob=None, store_name: str = "", location: str = "", employees_managed: int = 0) -> int:
        """Update store manager profile basic info"""
        sm = StoreManager.objects.get(storemanager_id=storemanager_id)
        sm.name = name
        sm.dob = dob
        sm.store_name = store_name
        sm.location = location
        sm.employees_managed = employees_managed
        sm.save()
        return sm.storemanager_id_id

    @staticmethod
    def remove(storemanager_id: int) -> None:
        """Delete store manager profile"""
        StoreManager.objects.get(storemanager_id=storemanager_id).delete()

    @staticmethod
    def get(storemanager_id: int) -> dict:
        """Fetch single store manager profile details"""
        return StoreManager.objects.filter(storemanager_id=storemanager_id).values(
            "storemanager_id", "name", "dob", "store_name", "location", "employees_managed", "created_date_time",
            "storemanager_id__username", "storemanager_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all store manager profiles (with optional search by name)"""
        from django.db.models import Q
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)

        return list(
            StoreManager.objects.filter(filters).values(
                "storemanager_id", "name", "dob", "store_name", "location", "employees_managed", "created_date_time",
                "storemanager_id__username", "storemanager_id__email"
            )
        )
