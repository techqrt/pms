from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User
from pms_apps.common.models.permissions import PropertyPermission


class MaintenanceManager(models.Model):
    manager_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="maintenance_manager_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    # e.g. HVAC, Electrical, Plumbing
    specialization = models.CharField(max_length=100, blank=True, null=True)
    team_size = models.IntegerField(default=0)
    years_of_experience = models.IntegerField(default=0)
    property_permission = models.ForeignKey(
        PropertyPermission, on_delete=models.DO_NOTHING, null=True)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "maintenance_manager"

    def __str__(self):
        return f"{self.name} ({self.manager_id.phone_number})"

    @staticmethod
    def get_permissions(user_id: int) -> dict:
        manager = MaintenanceManager.objects.filter(manager_id__user_id=user_id).first()

        permissions = {}
        if manager and manager.property_permission:
            permissions["property"] = manager.property_permission.property
            
        print(f"Permissions for user_id {user_id}: {permissions}")
        return {"permissions": permissions}

    def create(
        self,
        manager_id: int,
        name: str,
        dob: str,
        specialization: str,
        team_size: int,
        years_of_experience: int,
        property_permission_id: int,
    ) -> int:
        self.manager_id_id = manager_id
        self.name = name
        self.dob = dob
        self.specialization = specialization
        self.team_size = team_size
        self.years_of_experience = years_of_experience
        self.property_permission = PropertyPermission(property_permission_id)
        self.created_date_time = timezone.now()
        self.save()
        return self.manager_id_id

    @staticmethod
    def update(
        manager_id: int = None,
        name: str = None,
        dob: str = None,
        specialization: str = None,
        team_size: int = None,
        years_of_experience: int = None,
        property_permission_id: int = None,
    ) -> int:
        manager = MaintenanceManager.objects.get(manager_id=manager_id)
        if name is not None:
            manager.name = name
        if dob is not None:
            manager.dob = dob
        if specialization is not None:
            manager.specialization = specialization
        if team_size is not None:
            manager.team_size = team_size
        if years_of_experience is not None:
            manager.years_of_experience = years_of_experience
        if property_permission_id is not None:
            manager.property_permission_id = property_permission_id
        manager.save()
        return manager.manager_id_id

    @staticmethod
    def remove(manager_id: int) -> None:
        MaintenanceManager.objects.get(manager_id=manager_id).delete()

    @staticmethod
    def get(manager_id: int) -> dict:
        return MaintenanceManager.objects.filter(manager_id=manager_id).values(
            "manager_id", "name", "dob", "specialization", "team_size", "years_of_experience",
            "property_permission__permission_id", "property_permission__property",
            "created_date_time", "manager_id__phone_number", "manager_id__email"
        ).first()

    @staticmethod
    def get_all(
        sort_by: str = '',
        sort_order: str = '',
        filter_key: str = '',
        filter_value: str = '',
        search_key: str = '',
    ) -> list:
        data = MaintenanceManager.objects.all()
        if filter_key and filter_value:
            data = MaintenanceManager.objects.filter(
                **{f"{filter_key}__icontains": filter_value})
        if search_key:
            data = MaintenanceManager.objects.filter(
                Q(name__icontains=search_key) |
                Q(specialization__icontains=search_key)
            )
        if sort_by:
            data = data.order_by(
                ('-' if sort_order == 'desc' else '') + sort_by)
        return list(
            data.values(
                "manager_id", "name", "dob", "specialization", "team_size", "years_of_experience",
                "property_permission__permission_id", "property_permission__property",
                "created_date_time", "manager_id__phone_number", "manager_id__email"
            )
        )
