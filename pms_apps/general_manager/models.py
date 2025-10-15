from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User


class GeneralManager(models.Model):
    generalmanager_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="generalmanager_profile")
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    years_experience = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "general_manager"

    def __str__(self):
        return f"{self.name} ({self.generalmanager_id.phone_number})"

    # CRUD Operations
    def create(self, generalmanager_id: int, name: str, dob=None, department: str = "", years_experience: int = 0) -> int:
        self.generalmanager_id_id = generalmanager_id
        self.name = name
        self.dob = dob
        self.department = department
        self.years_experience = years_experience
        self.created_date_time = timezone.now()
        self.save()
        return self.generalmanager_id_id

    @staticmethod
    def update(generalmanager_id: int, name: str, dob=None, department: str = "", years_experience: int = 0) -> int:
        gm = GeneralManager.objects.get(generalmanager_id=generalmanager_id)
        gm.name = name
        gm.dob = dob
        gm.department = department
        gm.years_experience = years_experience
        gm.save()
        return gm.generalmanager_id_id

    @staticmethod
    def remove(generalmanager_id: int) -> None:
        GeneralManager.objects.get(generalmanager_id=generalmanager_id).delete()

    @staticmethod
    def get(generalmanager_id: int) -> dict:
        return GeneralManager.objects.filter(generalmanager_id=generalmanager_id).values(
            "generalmanager_id", "name", "dob", "department", "years_experience", "created_date_time",
            "generalmanager_id__phone_number", "generalmanager_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            GeneralManager.objects.filter(filters).values(
                "generalmanager_id", "name", "dob", "department", "years_experience", "created_date_time",
                "generalmanager_id__phone_number", "generalmanager_id__email"
            )
        )
