from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User


# ----------------------------
# Finance Manager
# ----------------------------
class FinanceManager(models.Model):
    manager_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="finance_manager_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    total_budget_managed = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    reports_submitted = models.IntegerField(default=0)
    team_size = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "finance_manager"

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
        total_budget_managed: float = 0.00,
        reports_submitted: int = 0,
        team_size: int = 0,
    ) -> int:
        """Create a new Finance Manager profile"""
        self.manager_id_id = manager_id
        self.name = name
        self.dob = dob
        self.department = department
        self.total_budget_managed = total_budget_managed
        self.reports_submitted = reports_submitted
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
        total_budget_managed: float = 0.00,
        reports_submitted: int = 0,
        team_size: int = 0,
    ) -> int:
        """Update finance manager profile"""
        m = FinanceManager.objects.get(manager_id=manager_id)
        m.name = name
        m.dob = dob
        m.department = department
        m.total_budget_managed = total_budget_managed
        m.reports_submitted = reports_submitted
        m.team_size = team_size
        m.save()
        return m.manager_id_id

    @staticmethod
    def remove(manager_id: int) -> None:
        """Delete finance manager profile"""
        FinanceManager.objects.get(manager_id=manager_id).delete()

    @staticmethod
    def get(manager_id: int) -> dict:
        """Fetch single finance manager profile"""
        return FinanceManager.objects.filter(manager_id=manager_id).values(
            "manager_id", "name", "dob", "department",
            "total_budget_managed", "reports_submitted", "team_size", "created_date_time",
            "manager_id__phone_number", "manager_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all finance managers"""
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            FinanceManager.objects.filter(filters).values(
                "manager_id", "name", "dob", "department",
                "total_budget_managed", "reports_submitted", "team_size", "created_date_time",
                "manager_id__phone_number", "manager_id__email"
            )
        )


# ----------------------------
# Finance Employee
# ----------------------------
class FinanceEmployee(models.Model):
    employee_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="finance_employee_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    role_title = models.CharField(max_length=100, blank=True, null=True)           # e.g., Accountant, Billing Executive
    invoices_processed = models.IntegerField(default=0)
    payments_verified = models.IntegerField(default=0)
    total_amount_handled = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    manager_ref = models.ForeignKey(FinanceManager, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "finance_employee"

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
        role_title: str = "",
        invoices_processed: int = 0,
        payments_verified: int = 0,
        total_amount_handled: float = 0.00,
        manager_ref: int = None,
    ) -> int:
        """Create a new Finance Employee profile"""
        self.employee_id_id = employee_id
        self.name = name
        self.dob = dob
        self.role_title = role_title
        self.invoices_processed = invoices_processed
        self.payments_verified = payments_verified
        self.total_amount_handled = total_amount_handled
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
        role_title: str = "",
        invoices_processed: int = 0,
        payments_verified: int = 0,
        total_amount_handled: float = 0.00,
        manager_ref: int = None,
    ) -> int:
        """Update finance employee profile"""
        e = FinanceEmployee.objects.get(employee_id=employee_id)
        e.name = name
        e.dob = dob
        e.role_title = role_title
        e.invoices_processed = invoices_processed
        e.payments_verified = payments_verified
        e.total_amount_handled = total_amount_handled
        if manager_ref is not None:
            e.manager_ref_id = manager_ref
        e.save()
        return e.employee_id_id

    @staticmethod
    def remove(employee_id: int) -> None:
        """Delete finance employee profile"""
        FinanceEmployee.objects.get(employee_id=employee_id).delete()

    @staticmethod
    def get(employee_id: int) -> dict:
        """Fetch single finance employee"""
        return FinanceEmployee.objects.filter(employee_id=employee_id).values(
            "employee_id", "name", "dob", "role_title", "invoices_processed",
            "payments_verified", "total_amount_handled", "manager_ref_id",
            "created_date_time", "employee_id__phone_number", "employee_id__email"
        ).first()

    @staticmethod
    def get_all(search_key: str = "") -> list:
        """Fetch all finance employees"""
        filters = Q()
        if search_key:
            filters &= Q(name__icontains=search_key)
        return list(
            FinanceEmployee.objects.filter(filters).values(
                "employee_id", "name", "dob", "role_title", "invoices_processed",
                "payments_verified", "total_amount_handled", "manager_ref_id",
                "created_date_time", "employee_id__phone_number", "employee_id__email"
            )
        )
