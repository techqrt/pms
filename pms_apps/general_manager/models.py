from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User


class GeneralManager(models.Model):
    general_manager_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="general_manager_profile")
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "general_manager"

    def __str__(self):
        return f"{self.name} ({self.general_manager_id.phone_number})"

    def create(
        self,
        general_manager_id: int,
        name: str,
        dob: str,
        department: str,
        years_of_experience: int
    ) -> int:
        self.general_manager_id_id = general_manager_id
        self.name = name
        self.dob = dob
        self.department = department
        self.years_of_experience = years_of_experience
        self.created_date_time = timezone.now()
        self.save()
        return self.general_manager_id_id

    @staticmethod
    def update(
        general_manager_id: int,
        name: str,
        dob: str,
        department: str,
        years_of_experience: int
    ) -> int:
        gm = GeneralManager.objects.get(general_manager_id=general_manager_id)
        gm.name = name
        gm.dob = dob
        gm.department = department
        gm.years_of_experience = years_of_experience
        gm.save()
        return gm.general_manager_id_id

    @staticmethod
    def remove(general_manager_id: int) -> None:
        GeneralManager.objects.get(general_manager_id=general_manager_id).delete()

    @staticmethod
    def get(general_manager_id: int) -> dict:
        return GeneralManager.objects.filter(general_manager_id=general_manager_id).values(
            "general_manager_id", "name", "dob", "department", "years_of_experience",
            "created_date_time", "general_manager_id__phone_number", "general_manager_id__email"
        ).first()

    @staticmethod
    def get_all(
        sort_by: str = '',
        sort_order: str = '',
        filter_key: str = '',
        filter_value: str = '',
        search_key: str = '',
    ) -> list:
        data = GeneralManager.objects.all()
        if filter_key and filter_value:
            data = GeneralManager.objects.filter(
                **{f"{filter_key}__icontains": filter_value})
        if search_key:
            data = GeneralManager.objects.filter(
                Q(name__icontains=search_key) |
                Q(department__icontains=search_key)
            )
        if sort_by:
            data = data.order_by(
                ('-' if sort_order == 'desc' else '') + sort_by)
        return list(
            data.values(
                "general_manager_id", "name", "dob", "department", "years_of_experience",
                "created_date_time", "general_manager_id__phone_number", "general_manager_id__email"
            )
        )
