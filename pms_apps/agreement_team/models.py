from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User


# ----------------------------
# Agreement Team Manager
# ----------------------------
class AgreementTeamManager(models.Model):
    manager_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="agreementteam_manager_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)         # e.g., Leasing, Contract Management
    specialization = models.CharField(max_length=100, blank=True, null=True)     # e.g., Rental, Vendor, Corporate
    agreements_handled = models.IntegerField(default=0)
    team_size = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "agreement_team_manager"

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
        department: str = "",
        specialization: str = "",
        agreements_handled: int = 0,
        team_size: int = 0,
    ) -> int:
        """Create a new Agreement Team Manager profile"""
        self.manager_id_id = manager_id
        self.name = name
        self.dob = dob
        self.department = department
        self.specialization = specialization
        self.agreements_handled = agreements_handled
        self.team_size = team_size
        self.created_date_time = timezone.now()
        self.save()
        return self.manager_id_id

    @staticmethod
    def update(
        manager_id: int,
        name: str,
        dob=None,
        department: str = "",
        specialization: str = "",
        agreements_handled: int = 0,
        team_size: int = 0,
    ) -> int:
        """Update Agreement Team Manager profile"""
        m = AgreementTeamManager.objects.get(manager_id=manager_id)
        m.name = name
        m.dob = dob
        m.department = department
        m.specialization = specialization
        m.agreements_handled = agreements_handled
        m.team_size = team_size
        m.save()
        return m.manager_id_id

    @staticmethod
    def remove(manager_id: int) -> None:
        """Delete Agreement Team Manager profile"""
        AgreementTeamManager.objects.get(manager_id=manager_id).delete()

    @staticmethod
    def get(manager_id: int) -> dict:
        """Fetch single Agreement Team Manager profile"""
        return AgreementTeamManager.objects.filter(manager_id=manager_id).values(
            "manager_id", "name", "dob", "department", "specialization", "agreements_handled",
            "team_size", "created_date_time", "manager_id__phone_number", "manager_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all Agreement Team Managers"""
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            AgreementTeamManager.objects.filter(filters).values(
                "manager_id", "name", "dob", "department", "specialization", "agreements_handled",
                "team_size", "created_date_time", "manager_id__phone_number", "manager_id__email"
            )
        )


# ----------------------------
# Agreement Team Employee
# ----------------------------
class AgreementTeamEmployee(models.Model):
    employee_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="agreementteam_employee_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)       # e.g., Contracts, Leasing
    specialization = models.CharField(max_length=100, blank=True, null=True)   # e.g., Rental Agreements, Corporate Contracts
    agreements_handled = models.IntegerField(default=0)                        # Count of agreements/contracts
    manager_ref = models.ForeignKey(AgreementTeamManager, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "agreement_team_employee"

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
        department: str = "",
        specialization: str = "",
        agreements_handled: int = 0,
        manager_ref: int = None,
    ) -> int:
        """Create a new Agreement Team Employee profile"""
        self.employee_id_id = employee_id
        self.name = name
        self.dob = dob
        self.department = department
        self.specialization = specialization
        self.agreements_handled = agreements_handled
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
        department: str = "",
        specialization: str = "",
        agreements_handled: int = 0,
        manager_ref: int = None,
    ) -> int:
        """Update Agreement Team Employee profile"""
        e = AgreementTeamEmployee.objects.get(employee_id=employee_id)
        e.name = name
        e.dob = dob
        e.department = department
        e.specialization = specialization
        e.agreements_handled = agreements_handled
        if manager_ref is not None:
            e.manager_ref_id = manager_ref
        e.save()
        return e.employee_id_id

    @staticmethod
    def remove(employee_id: int) -> None:
        """Delete Agreement Team Employee profile"""
        AgreementTeamEmployee.objects.get(employee_id=employee_id).delete()

    @staticmethod
    def get(employee_id: int) -> dict:
        """Fetch single Agreement Team Employee"""
        return AgreementTeamEmployee.objects.filter(employee_id=employee_id).values(
            "employee_id", "name", "dob", "department", "specialization", "agreements_handled",
            "manager_ref_id", "created_date_time", "employee_id__phone_number", "employee_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all Agreement Team Employees"""
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            AgreementTeamEmployee.objects.filter(filters).values(
                "employee_id", "name", "dob", "department", "specialization", "agreements_handled",
                "manager_ref_id", "created_date_time", "employee_id__phone_number", "employee_id__email"
            )
        )
