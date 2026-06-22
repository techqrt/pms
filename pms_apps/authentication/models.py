from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from datetime import timedelta
from django.utils import timezone

from django.utils.timezone import now
from django.core.validators import RegexValidator


class User(AbstractBaseUser):
    DEPARTMENT_CHOICES = [
        ("Tenant", "Tenant"),
        ("Landlord", "Landlord"),
        ("Marketing", "Marketing"),
        ("Property", "Property"),
        ("Maintenance", "Maintenance"),
        ("Reception", "Reception"),
        ("Finance", "Finance"),
        ("Collection", "Collection"),
        ("Legal", "Legal"),
        ("IT", "IT"),
        ("General Manager", "General Manager"),
        ("HR", "HR"),
        ("Owner", "Owner"),
        ("Check-In Check-Out", "Check-In Check-Out"),
    ]

    ROLE_CHOICES = [
        ("Owner", "Owner"),
        ("General Manager", "General Manager"),
        ("Manager", "Manager"),
        ("Employee", "Employee"),
        ("Technician", "Technician"),
    ]

    user_id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100, default="")
    email = models.EmailField(blank=True, null=True)
    department = models.CharField(
        max_length=100, choices=DEPARTMENT_CHOICES, blank=True, null=True)
    role = models.CharField(
        max_length=50, choices=ROLE_CHOICES, blank=True, null=True)
    access_token = models.TextField(default='')
    refresh_token = models.TextField(default='')
    otp = models.IntegerField(null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.name or self.phone_number} ({self.department or 'No Dept'})"

    def get_permissions(self):
        from pms_apps.lead.models.lead import Lead
        from pms_apps.marketing.models.marketing_employee import MarketingEmployee
        from pms_apps.marketing.models.marketing_manager import MarketingManager
        from pms_apps.maintenance.models.maintenance_employee import MaintenanceEmployee
        from pms_apps.maintenance.models.maintenance_manager import MaintenanceManager
        from pms_apps.maintenance.models.maintenance_technician import MaintenanceTechnician

        permission_map = {
            "Tenant": lambda: Lead.get_permissions(user_id=self.user_id),
            "Marketing": lambda: (
                MarketingManager.get_permissions(user_id=self.user_id)
                if self.role == "Manager"
                else MarketingEmployee.get_permissions(user_id=self.user_id)
            ),
            "Maintenance": lambda: (
                MaintenanceTechnician.get_permissions(user_id=self.user_id)
                if self.role == "Technician"
                else MaintenanceManager.get_permissions(user_id=self.user_id)
                if self.role == "Manager"
                else MaintenanceEmployee.get_permissions(user_id=self.user_id)
            ),
        }

        permission_func = permission_map.get(self.department)
        if not permission_func:
            return {}

        permissions = permission_func().get("permissions", {})
        return permissions

    # Optional helper for OTP generation

    def generate_otp(self):
        import random
        otp = random.randint(100000, 999999)
        self.otp = otp
        self.otp_expiry = timezone.now() + timezone.timedelta(minutes=10)
        self.save()
        return otp

    def get(user_id: int) -> dict:
        user = User.objects.filter(user_id=user_id).values(
            'user_id', 'phone_number', 'name', 'email', 'department', 'role', 'access_token').first()
        return user
