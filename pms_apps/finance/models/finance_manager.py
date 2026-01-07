from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User


class FinanceManager(models.Model):
    manager_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="finance_manager_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    total_budget_managed = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00)
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
        dob: str,
        department: str,
        total_budget_managed: float,
        reports_submitted: int,
        team_size: int,
    ) -> int:
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
        dob: str,
        department: str,
        total_budget_managed: float,
        reports_submitted: int,
        team_size: int,
    ) -> int:
        manager = FinanceManager.objects.get(manager_id=manager_id)
        manager.name = name
        manager.dob = dob
        manager.department = department
        manager.total_budget_managed = total_budget_managed
        manager.reports_submitted = reports_submitted
        manager.team_size = team_size
        manager.save()
        return manager.manager_id_id

    @staticmethod
    def remove(manager_id: int) -> None:
        FinanceManager.objects.get(manager_id=manager_id).delete()

    @staticmethod
    def get(manager_id: int) -> dict:
        return FinanceManager.objects.filter(manager_id=manager_id).values(
            "manager_id", "name", "dob", "department", "total_budget_managed", "reports_submitted", "team_size",
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
        data = FinanceManager.objects.all()
        if filter_key and filter_value:
            data = FinanceManager.objects.filter(
                **{f"{filter_key}__icontains": filter_value})
        if search_key:
            data = FinanceManager.objects.filter(
                Q(name__icontains=search_key) |
                Q(department__icontains=search_key)
            )
        if sort_by:
            data = data.order_by(
                ('-' if sort_order == 'desc' else '') + sort_by)
        return list(
            data.values(
                "manager_id", "name", "dob", "department", "total_budget_managed", "reports_submitted", "team_size",
                "created_date_time", "manager_id__phone_number", "manager_id__email"
            )
        )
