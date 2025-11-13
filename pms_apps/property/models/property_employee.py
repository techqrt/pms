from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User
from pms_apps.property.models.property_manager import PropertyManager

class PropertyEmployee(models.Model):
    employee_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="property_employee_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    assigned_units = models.IntegerField(default=0)
    region = models.CharField(max_length=100, blank=True, null=True)
    manager_ref = models.ForeignKey(PropertyManager, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "property_employee"

    def __str__(self):
        return f"{self.name} ({self.employee_id.phone_number})"

    # ----------------------
    # CRUD Operations
    # ----------------------

    def create(
        self,
        employee_id: int,
        name: str,
        dob=None,
        designation: str = "",
        assigned_units: int = 0,
        region: str = "",
        manager_ref: int = None,
    ) -> int:
        """Create new Property Employee"""
        self.employee_id_id = employee_id
        self.name = name
        self.dob = dob
        self.designation = designation
        self.assigned_units = assigned_units
        self.region = region
        if manager_ref:
            self.manager_ref_id = manager_ref
        self.created_date_time = timezone.now()
        self.save()
        return self.employee_id_id

    @staticmethod
    def update(
        employee_id: int,
        name: str,
        dob=None,
        designation: str = "",
        assigned_units: int = 0,
        region: str = "",
        manager_ref: int = None,
    ) -> int:
        """Update Property Employee"""
        e = PropertyEmployee.objects.get(employee_id=employee_id)
        e.name = name
        e.dob = dob
        e.designation = designation
        e.assigned_units = assigned_units
        e.region = region
        if manager_ref is not None:
            e.manager_ref_id = manager_ref
        e.save()
        return e.employee_id_id

    @staticmethod
    def remove(employee_id: int) -> None:
        """Delete Property Employee"""
        PropertyEmployee.objects.get(employee_id=employee_id).delete()

    @staticmethod
    def get(employee_id: int) -> dict:
        """Fetch single Property Employee"""
        return PropertyEmployee.objects.filter(employee_id=employee_id).values(
            "employee_id",
            "name",
            "dob",
            "designation",
            "assigned_units",
            "region",
            "manager_ref_id",
            "created_date_time",
            "employee_id__phone_number",
            "employee_id__email",
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all Property Employees"""
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            PropertyEmployee.objects.filter(filters).values(
                "employee_id",
                "name",
                "dob",
                "designation",
                "assigned_units",
                "region",
                "manager_ref_id",
                "created_date_time",
                "employee_id__phone_number",
                "employee_id__email",
            )
        )
