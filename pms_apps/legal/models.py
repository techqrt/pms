from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User


# ----------------------------
# Legal Manager
# ----------------------------
class LegalManager(models.Model):
    manager_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="legal_manager_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    total_cases_handled = models.IntegerField(default=0)
    open_cases = models.IntegerField(default=0)
    closed_cases = models.IntegerField(default=0)
    team_size = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "legal_manager"

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
        total_cases_handled: int = 0,
        open_cases: int = 0,
        closed_cases: int = 0,
        team_size: int = 0,
    ) -> int:
        """Create a new Legal Manager profile"""
        self.manager_id_id = manager_id
        self.name = name
        self.dob = dob
        self.department = department
        self.total_cases_handled = total_cases_handled
        self.open_cases = open_cases
        self.closed_cases = closed_cases
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
        total_cases_handled: int = 0,
        open_cases: int = 0,
        closed_cases: int = 0,
        team_size: int = 0,
    ) -> int:
        """Update legal manager profile"""
        m = LegalManager.objects.get(manager_id=manager_id)
        m.name = name
        m.dob = dob
        m.department = department
        m.total_cases_handled = total_cases_handled
        m.open_cases = open_cases
        m.closed_cases = closed_cases
        m.team_size = team_size
        m.save()
        return m.manager_id_id

    @staticmethod
    def remove(manager_id: int) -> None:
        """Delete legal manager profile"""
        LegalManager.objects.get(manager_id=manager_id).delete()

    @staticmethod
    def get(manager_id: int) -> dict:
        """Fetch single legal manager profile"""
        return LegalManager.objects.filter(manager_id=manager_id).values(
            "manager_id", "name", "dob", "department", "total_cases_handled",
            "open_cases", "closed_cases", "team_size", "created_date_time",
            "manager_id__phone_number", "manager_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all legal managers"""
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            LegalManager.objects.filter(filters).values(
                "manager_id", "name", "dob", "department", "total_cases_handled",
                "open_cases", "closed_cases", "team_size", "created_date_time",
                "manager_id__phone_number", "manager_id__email"
            )
        )


# ----------------------------
# Legal Employee
# ----------------------------
class LegalEmployee(models.Model):
    employee_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="legal_employee_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    designation = models.CharField(max_length=100, blank=True, null=True)   # e.g., Legal Assistant, Paralegal
    active_cases = models.IntegerField(default=0)
    case_specialization = models.CharField(max_length=100, blank=True, null=True)  # e.g., Civil, Corporate, Contract
    manager_ref = models.ForeignKey(LegalManager, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "legal_employee"

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
        active_cases: int = 0,
        case_specialization: str = "",
        manager_ref: int = None,
    ) -> int:
        """Create a new Legal Employee profile"""
        self.employee_id_id = employee_id
        self.name = name
        self.dob = dob
        self.designation = designation
        self.active_cases = active_cases
        self.case_specialization = case_specialization
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
        active_cases: int = 0,
        case_specialization: str = "",
        manager_ref: int = None,
    ) -> int:
        """Update legal employee profile"""
        e = LegalEmployee.objects.get(employee_id=employee_id)
        e.name = name
        e.dob = dob
        e.designation = designation
        e.active_cases = active_cases
        e.case_specialization = case_specialization
        if manager_ref is not None:
            e.manager_ref_id = manager_ref
        e.save()
        return e.employee_id_id

    @staticmethod
    def remove(employee_id: int) -> None:
        """Delete legal employee profile"""
        LegalEmployee.objects.get(employee_id=employee_id).delete()

    @staticmethod
    def get(employee_id: int) -> dict:
        """Fetch single legal employee profile"""
        return LegalEmployee.objects.filter(employee_id=employee_id).values(
            "employee_id", "name", "dob", "designation", "active_cases", "case_specialization",
            "manager_ref_id", "created_date_time", "employee_id__phone_number", "employee_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all legal employees"""
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            LegalEmployee.objects.filter(filters).values(
                "employee_id", "name", "dob", "designation", "active_cases", "case_specialization",
                "manager_ref_id", "created_date_time", "employee_id__phone_number", "employee_id__email"
            )
        )
