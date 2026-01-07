from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User
from pms_apps.common.models.permissions import PropertyPermission


class MaintenanceTechnician(models.Model):
    technician_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="maintenance_technician_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    # e.g. Electrician, Plumber, Carpenter
    skill_type = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.IntegerField(default=0)
    assigned_jobs = models.IntegerField(default=0)
    property_permission = models.ForeignKey(
        PropertyPermission, on_delete=models.DO_NOTHING, null=True)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "maintenance_technician"

    def __str__(self):
        return f"{self.name} ({self.technician_id.phone_number})"

    @staticmethod
    def get_permissions(user_id: int) -> dict:
        technician = MaintenanceTechnician.objects.filter(
            technician_id__user_id=user_id).first()

        permissions = {}
        if technician and technician.property_permission:
            permissions["property"] = technician.property_permission.property

        return {"permissions": permissions}

    def create(
        self,
        technician_id: int,
        name: str,
        dob: str,
        skill_type: str,
        years_of_experience: int,
        assigned_jobs: int,
        property_permission_id: int,
    ) -> int:
        self.technician_id_id = technician_id
        self.name = name
        self.dob = dob
        self.skill_type = skill_type
        self.years_of_experience = years_of_experience
        self.assigned_jobs = assigned_jobs
        self.property_permission = PropertyPermission(property_permission_id)
        self.created_date_time = timezone.now()
        self.save()
        return self.technician_id_id

    @staticmethod
    def update(
        technician_id: int = None,
        name: str = None,
        dob: str = None,
        skill_type: str = None,
        years_of_experience: int = None,
        assigned_jobs: int = None,
        property_permission_id: int = None,
    ) -> int:
        technician = MaintenanceTechnician.objects.get(
            technician_id=technician_id)
        if name is not None:
            technician.name = name
        if dob is not None:
            technician.dob = dob
        if skill_type is not None:
            technician.skill_type = skill_type
        if years_of_experience is not None:
            technician.years_of_experience = years_of_experience
        if assigned_jobs is not None:
            technician.assigned_jobs = assigned_jobs
        if property_permission_id is not None:
            technician.property_permission_id = property_permission_id
        technician.save()
        return technician.technician_id_id

    @staticmethod
    def remove(technician_id: int) -> None:
        MaintenanceTechnician.objects.get(technician_id=technician_id).delete()

    @staticmethod
    def get(technician_id: int) -> dict:
        return MaintenanceTechnician.objects.filter(technician_id=technician_id).values(
            "technician_id", "name", "dob", "skill_type", "years_of_experience", "assigned_jobs",
            "property_permission__permission_id", "property_permission__property",
            "created_date_time", "technician_id__phone_number", "technician_id__email"
        ).first()

    @staticmethod
    def get_all(
        sort_by: str = '',
        sort_order: str = '',
        filter_key: str = '',
        filter_value: str = '',
        search_key: str = '',
    ) -> list:
        data = MaintenanceTechnician.objects.all()
        if filter_key and filter_value:
            data = MaintenanceTechnician.objects.filter(
                **{f"{filter_key}__icontains": filter_value})
        if search_key:
            data = MaintenanceTechnician.objects.filter(
                Q(name__icontains=search_key) |
                Q(skill_type__icontains=search_key)
            )
        if sort_by:
            data = data.order_by(
                ('-' if sort_order == 'desc' else '') + sort_by)
        return list(
            data.values(
                "technician_id", "name", "dob", "skill_type", "years_of_experience", "assigned_jobs",
                "property_permission__permission_id", "property_permission__property",
                "created_date_time", "technician_id__phone_number", "technician_id__email"
            )
        )
