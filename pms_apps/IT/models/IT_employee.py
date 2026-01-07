from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User
from pms_apps.IT.models.IT_manager import ITManager


class ITEmployee(models.Model):
    employee_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="it_employee_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    # e.g., Developer, SysAdmin
    role_title = models.CharField(max_length=100, blank=True, null=True)
    tickets_resolved = models.IntegerField(default=0)
    projects_assigned = models.IntegerField(default=0)
    specialization = models.CharField(
        max_length=100, blank=True, null=True)  # e.g., Backend, Networking
    manager_ref = models.ForeignKey(
        ITManager, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "it_employee"

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
        tickets_resolved: int,
        projects_assigned: int,
        specialization: str,
        manager_ref: int,
    ) -> int:
        self.employee_id_id = employee_id
        self.name = name
        self.dob = dob
        self.role_title = role_title
        self.tickets_resolved = tickets_resolved
        self.projects_assigned = projects_assigned
        self.specialization = specialization
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
        tickets_resolved: int,
        projects_assigned: int,
        specialization: str,
        manager_ref: int,
    ) -> int:
        employee = ITEmployee.objects.get(employee_id=employee_id)
        employee.name = name
        employee.dob = dob
        employee.role_title = role_title
        employee.tickets_resolved = tickets_resolved
        employee.projects_assigned = projects_assigned
        employee.specialization = specialization
        if manager_ref is not None:
            employee.manager_ref_id = manager_ref
        employee.save()
        return employee.employee_id_id

    @staticmethod
    def remove(employee_id: int) -> None:
        ITEmployee.objects.get(employee_id=employee_id).delete()

    @staticmethod
    def get(employee_id: int) -> dict:
        return ITEmployee.objects.filter(employee_id=employee_id).values(
            "employee_id", "name", "dob", "role_title", "tickets_resolved", "projects_assigned", "specialization",
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
        """Fetch all marketing employees"""
        data = ITEmployee.objects.all()
        if filter_key and filter_value:
            data = ITEmployee.objects.filter(
                **{f"{filter_key}__icontains": filter_value})
        if search_key:
            data = ITEmployee.objects.filter(
                Q(name__icontains=search_key) |
                Q(role_title__icontains=search_key) |
                Q(specialization__icontains=search_key)
            )
        if sort_by:
            data = data.order_by(
                ('-' if sort_order == 'desc' else '') + sort_by)
        return list(
            data.values(
                "employee_id", "name", "dob", "role_title", "tickets_resolved", "projects_assigned", "specialization",
                "manager_ref_id", "created_date_time", "employee_id__phone_number", "employee_id__email"
            )
        )
