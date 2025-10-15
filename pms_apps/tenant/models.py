# pms_apps/tenant/models.py
from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User


class Tenant(models.Model):
    tenant_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="tenant_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    lease_start = models.DateField(null=True, blank=True)
    lease_end = models.DateField(null=True, blank=True)
    property_name = models.CharField(max_length=150, blank=True, null=True)
    rent_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "tenant"

    def __str__(self):
        return f"{self.name} ({self.tenant_id.phone_number})"

    # CRUD
    def create(
        self,
        tenant_id: int,
        name: str,
        dob=None,
        address: str = "",
        lease_start=None,
        lease_end=None,
        property_name: str = "",
        rent_amount: float = 0.0,
    ) -> int:
        self.tenant_id_id = tenant_id
        self.name = name
        self.dob = dob
        self.address = address
        self.lease_start = lease_start
        self.lease_end = lease_end
        self.property_name = property_name
        self.rent_amount = rent_amount
        self.created_date_time = timezone.now()
        self.save()
        return self.tenant_id_id

    @staticmethod
    def update(
        tenant_id: int,
        name: str,
        dob=None,
        address: str = "",
        lease_start=None,
        lease_end=None,
        property_name: str = "",
        rent_amount: float = 0.0,
    ) -> int:
        tenant = Tenant.objects.get(tenant_id=tenant_id)
        tenant.name = name
        tenant.dob = dob
        tenant.address = address
        tenant.lease_start = lease_start
        tenant.lease_end = lease_end
        tenant.property_name = property_name
        tenant.rent_amount = rent_amount
        tenant.save()
        return tenant.tenant_id_id

    @staticmethod
    def remove(tenant_id: int) -> None:
        Tenant.objects.get(tenant_id=tenant_id).delete()

    @staticmethod
    def get(tenant_id: int) -> dict:
        return Tenant.objects.filter(tenant_id=tenant_id).values(
            "tenant_id",
            "name",
            "dob",
            "address",
            "lease_start",
            "lease_end",
            "property_name",
            "rent_amount",
            "created_date_time",
            "tenant_id__phone_number",
            "tenant_id__email",
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            Tenant.objects.filter(filters).values(
                "tenant_id",
                "name",
                "dob",
                "address",
                "lease_start",
                "lease_end",
                "property_name",
                "rent_amount",
                "created_date_time",
                "tenant_id__phone_number",
                "tenant_id__email",
            )
        )


class TenantManager(models.Model):
    manager_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="tenant_manager_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)  # optional metadata
    team_size = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "tenant_manager"

    def __str__(self):
        return f"{self.name} ({self.manager_id.phone_number})"

    # CRUD
    def create(self, manager_id: int, name: str, dob=None, department: str = "", team_size: int = 0) -> int:
        self.manager_id_id = manager_id
        self.name = name
        self.dob = dob
        self.department = department
        self.team_size = team_size
        self.created_date_time = timezone.now()
        self.save()
        return self.manager_id_id

    @staticmethod
    def update(manager_id: int, name: str, dob=None, department: str = "", team_size: int = 0) -> int:
        m = TenantManager.objects.get(manager_id=manager_id)
        m.name = name
        m.dob = dob
        m.department = department
        m.team_size = team_size
        m.save()
        return m.manager_id_id

    @staticmethod
    def remove(manager_id: int) -> None:
        TenantManager.objects.get(manager_id=manager_id).delete()

    @staticmethod
    def get(manager_id: int) -> dict:
        return TenantManager.objects.filter(manager_id=manager_id).values(
            "manager_id", "name", "dob", "department", "team_size", "created_date_time",
            "manager_id__phone_number", "manager_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            TenantManager.objects.filter(filters).values(
                "manager_id", "name", "dob", "department", "team_size", "created_date_time",
                "manager_id__phone_number", "manager_id__email"
            )
        )


class TenantEmployee(models.Model):
    employee_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="tenant_employee_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    manager_ref = models.ForeignKey(TenantManager, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "tenant_employee"

    def __str__(self):
        return f"{self.name} ({self.employee_id.phone_number})"

    # CRUD
    def create(self, employee_id: int, name: str, dob=None, designation: str = "", manager_ref: int = None) -> int:
        self.employee_id_id = employee_id
        self.name = name
        self.dob = dob
        self.designation = designation
        if manager_ref:
            self.manager_ref_id = manager_ref
        self.created_date_time = timezone.now()
        self.save()
        return self.employee_id_id

    @staticmethod
    def update(employee_id: int, name: str, dob=None, designation: str = "", manager_ref: int = None) -> int:
        e = TenantEmployee.objects.get(employee_id=employee_id)
        e.name = name
        e.dob = dob
        e.designation = designation
        if manager_ref is not None:
            e.manager_ref_id = manager_ref
        e.save()
        return e.employee_id_id

    @staticmethod
    def remove(employee_id: int) -> None:
        TenantEmployee.objects.get(employee_id=employee_id).delete()

    @staticmethod
    def get(employee_id: int) -> dict:
        return TenantEmployee.objects.filter(employee_id=employee_id).values(
            "employee_id", "name", "dob", "designation", "manager_ref_id", "created_date_time",
            "employee_id__phone_number", "employee_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            TenantEmployee.objects.filter(filters).values(
                "employee_id", "name", "dob", "designation", "manager_ref_id", "created_date_time",
                "employee_id__phone_number", "employee_id__email"
            )
        )
