from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User
from pms_apps.finance.models.finance_manager import FinanceManager


class FinanceEmployee(models.Model):
    employee_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="finance_employee_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    # e.g., Accountant, Billing Executive
    role_title = models.CharField(max_length=100, blank=True, null=True)
    invoices_processed = models.IntegerField(default=0)
    payments_verified = models.IntegerField(default=0)
    total_amount_handled = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00)
    manager_ref = models.ForeignKey(
        FinanceManager, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
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
        dob: str,
        role_title: str,
        invoices_processed: int,
        payments_verified: int,
        total_amount_handled: float,
        manager_ref: int,
    ) -> int:
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
        dob: str,
        role_title: str,
        invoices_processed: int,
        payments_verified: int,
        total_amount_handled: float,
        manager_ref: int,
    ) -> int:
        employee = FinanceEmployee.objects.get(employee_id=employee_id)
        employee.name = name
        employee.dob = dob
        employee.role_title = role_title
        employee.invoices_processed = invoices_processed
        employee.payments_verified = payments_verified
        employee.total_amount_handled = total_amount_handled
        if manager_ref is not None:
            employee.manager_ref_id = manager_ref
        employee.save()
        return employee.employee_id_id

    @staticmethod
    def remove(employee_id: int) -> None:
        FinanceEmployee.objects.get(employee_id=employee_id).delete()

    @staticmethod
    def get(employee_id: int) -> dict:
        return FinanceEmployee.objects.filter(employee_id=employee_id).values(
            "employee_id", "name", "dob", "role_title", "invoices_processed", "payments_verified", "total_amount_handled",
            "manager_ref_id", "created_date_time", "employee_id__phone_number", "employee_id__email"
        ).first()

    @staticmethod
    def get_all(
        sort_by: str = '',
        sort_order: str = '',
        filter_key: str = '',
        filter_value: str = '',
        search_key: str = '',
    ) -> list:
        data = FinanceEmployee.objects.all()
        if filter_key and filter_value:
            data = FinanceEmployee.objects.filter(
                **{f"{filter_key}__icontains": filter_value})
        if search_key:
            data = FinanceEmployee.objects.filter(
                Q(name__icontains=search_key) |
                Q(role_title__icontains=search_key)
            )
        if sort_by:
            data = data.order_by(
                ('-' if sort_order == 'desc' else '') + sort_by)
        return list(
            data.values(
                "employee_id", "name", "dob", "role_title", "invoices_processed", "payments_verified", "total_amount_handled",
                "manager_ref_id", "created_date_time", "employee_id__phone_number", "employee_id__email"
            )
        )
