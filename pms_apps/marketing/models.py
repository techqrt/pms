from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User


class MarketingManager(models.Model):
    manager_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="marketing_manager_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)       # e.g. Digital, Field Marketing
    campaigns_led = models.IntegerField(default=0)
    team_size = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "marketing_manager"

    def __str__(self):
        return f"{self.name} ({self.manager_id.phone_number})"

    # ----------------------
    # Static CRUD Operations
    # ----------------------

    def create(
        self,
        manager_id: int,
        name: str,
        dob=None,
        department: str = "",
        campaigns_led: int = 0,
        team_size: int = 0,
    ) -> int:
        """Create a new Marketing Manager profile"""
        self.manager_id_id = manager_id
        self.name = name
        self.dob = dob
        self.department = department
        self.campaigns_led = campaigns_led
        self.team_size = team_size
        self.created_date_time = timezone.now()
        self.save()
        return self.manager_id_id

    @staticmethod
    def update(manager_id: int, name: str, dob=None, department: str = "", campaigns_led: int = 0, team_size: int = 0) -> int:
        """Update marketing manager profile"""
        m = MarketingManager.objects.get(manager_id=manager_id)
        m.name = name
        m.dob = dob
        m.department = department
        m.campaigns_led = campaigns_led
        m.team_size = team_size
        m.save()
        return m.manager_id_id

    @staticmethod
    def remove(manager_id: int) -> None:
        """Delete marketing manager profile"""
        MarketingManager.objects.get(manager_id=manager_id).delete()

    @staticmethod
    def get(manager_id: int) -> dict:
        """Fetch single marketing manager profile"""
        return MarketingManager.objects.filter(manager_id=manager_id).values(
            "manager_id", "name", "dob", "department", "campaigns_led", "team_size", "created_date_time",
            "manager_id__phone_number", "manager_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all marketing managers"""
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            MarketingManager.objects.filter(filters).values(
                "manager_id", "name", "dob", "department", "campaigns_led", "team_size", "created_date_time",
                "manager_id__phone_number", "manager_id__email"
            )
        )


class MarketingEmployee(models.Model):
    employee_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="marketing_employee_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    campaigns_assigned = models.IntegerField(default=0)
    leads_generated = models.IntegerField(default=0)
    manager_ref = models.ForeignKey(MarketingManager, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "marketing_employee"

    def __str__(self):
        return f"{self.name} ({self.employee_id.phone_number})"

    # ----------------------
    # Static CRUD Operations
    # ----------------------

    def create(
        self,
        employee_id: int,
        name: str,
        dob=None,
        designation: str = "",
        department: str = "",
        campaigns_assigned: int = 0,
        leads_generated: int = 0,
        manager_ref: int = None,
    ) -> int:
        """Create a new Marketing Employee profile"""
        self.employee_id_id = employee_id
        self.name = name
        self.dob = dob
        self.designation = designation
        self.department = department
        self.campaigns_assigned = campaigns_assigned
        self.leads_generated = leads_generated
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
        department: str = "",
        campaigns_assigned: int = 0,
        leads_generated: int = 0,
        manager_ref: int = None,
    ) -> int:
        """Update marketing employee profile"""
        e = MarketingEmployee.objects.get(employee_id=employee_id)
        e.name = name
        e.dob = dob
        e.designation = designation
        e.department = department
        e.campaigns_assigned = campaigns_assigned
        e.leads_generated = leads_generated
        if manager_ref is not None:
            e.manager_ref_id = manager_ref
        e.save()
        return e.employee_id_id

    @staticmethod
    def remove(employee_id: int) -> None:
        """Delete marketing employee"""
        MarketingEmployee.objects.get(employee_id=employee_id).delete()

    @staticmethod
    def get(employee_id: int) -> dict:
        """Fetch single marketing employee profile"""
        return MarketingEmployee.objects.filter(employee_id=employee_id).values(
            "employee_id", "name", "dob", "designation", "department",
            "campaigns_assigned", "leads_generated", "manager_ref_id",
            "created_date_time", "employee_id__phone_number", "employee_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all marketing employees"""
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            MarketingEmployee.objects.filter(filters).values(
                "employee_id", "name", "dob", "designation", "department",
                "campaigns_assigned", "leads_generated", "manager_ref_id",
                "created_date_time", "employee_id__phone_number", "employee_id__email"
            )
        )
