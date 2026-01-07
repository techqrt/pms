from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User
from pms_apps.collection.models.collection_manager import CollectionManager


class CollectionEmployee(models.Model):
    employee_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="collection_employee_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    # e.g., Field Collector, Recovery Officer
    designation = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    collections_made = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00)
    overdue_accounts_handled = models.IntegerField(default=0)
    manager_ref = models.ForeignKey(
        CollectionManager, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "collection_employee"

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
        designation: str,
        region: str,
        collections_made: float,
        overdue_accounts_handled: int,
        manager_ref: int,
    ) -> int:
        self.employee_id_id = employee_id
        self.name = name
        self.dob = dob
        self.designation = designation
        self.region = region
        self.collections_made = collections_made
        self.overdue_accounts_handled = overdue_accounts_handled
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
        designation: str,
        region: str,
        collections_made: float,
        overdue_accounts_handled: int,
        manager_ref: int,
    ) -> int:
        employee = CollectionEmployee.objects.get(employee_id=employee_id)
        employee.name = name
        employee.dob = dob
        employee.designation = designation
        employee.region = region
        employee.collections_made = collections_made
        employee.overdue_accounts_handled = overdue_accounts_handled
        if manager_ref is not None:
            employee.manager_ref_id = manager_ref
        employee.save()
        return employee.employee_id_id

    @staticmethod
    def remove(employee_id: int) -> None:
        CollectionEmployee.objects.get(employee_id=employee_id).delete()

    @staticmethod
    def get(employee_id: int) -> dict:
        return CollectionEmployee.objects.filter(employee_id=employee_id).values(
            "employee_id", "name", "dob", "designation", "region", "collections_made", "overdue_accounts_handled",
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
        data = CollectionEmployee.objects.all()
        if filter_key and filter_value:
            data = CollectionEmployee.objects.filter(
                **{f"{filter_key}__icontains": filter_value})
        if search_key:
            data = CollectionEmployee.objects.filter(
                Q(name__icontains=search_key) |
                Q(shift__icontains=search_key) |
                Q(desk_number__icontains=search_key)
            )
        if sort_by:
            data = data.order_by(
                ('-' if sort_order == 'desc' else '') + sort_by)
        return list(
            data.values(
                "employee_id", "name", "dob", "designation", "region", "collections_made", "overdue_accounts_handled",
                "manager_ref_id", "created_date_time", "employee_id__phone_number", "employee_id__email"
            )
        )
