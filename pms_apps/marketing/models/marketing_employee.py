from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User
from pms_apps.marketing.models.marketing_manager import MarketingManager
from pms_apps.common.models.permissions import LeadPermission,PropertyPermission


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
    manager_ref = models.ForeignKey(
        MarketingManager, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="marketing_employee_manager_ref"
    )
    lead_permission = models.ForeignKey(
        LeadPermission,
        on_delete=models.DO_NOTHING,
        null=True
    )
    property_permission = models.ForeignKey(
        PropertyPermission,
        on_delete=models.DO_NOTHING,
        null=True
    )
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "marketing_employee"

    def __str__(self):
        return f"{self.name} ({self.employee_id.phone_number})"

    @staticmethod
    def get_permissions(user_id : int) -> dict:
        employee = MarketingEmployee.objects.filter(employee_id = user_id).first()

        permissions = {}
        if employee :
            if employee.lead_permission:
                permissions["lead"] = employee.lead_permission.lead
            if employee.property_permission:
                permissions["property"] = employee.property_permission.property
        return {
            "permissions" : permissions
        }

    def create(
        self,
        employee_id: int,
        name: str,
        dob: str,
        designation: str,
        department: str,
        campaigns_assigned: int,
        leads_generated: int,
        manager_ref: int,
        lead_permission_id : int,
        property_permission_id : int,
    ) -> int:
        self.employee_id_id = employee_id
        self.name = name
        self.dob = dob
        self.designation = designation
        self.department = department
        self.campaigns_assigned = campaigns_assigned
        self.leads_generated = leads_generated
        if manager_ref:
            self.manager_ref_id = manager_ref
        self.lead_permission = LeadPermission(lead_permission_id)
        self.property_permission = PropertyPermission(property_permission_id)
        self.created_date_time = timezone.now()
        self.save()
        return self.employee_id_id

    @staticmethod
    def update(
        employee_id: int = None,
        name: str = None,
        dob: str = None,
        designation: str = None,
        department: str = None,
        campaigns_assigned: int = None,
        leads_generated: int = None,
        manager_ref: int = None,
        lead_permission_id: int = None,
        property_permission_id: int = None,
    ) -> int:
        employee = MarketingEmployee.objects.get(employee_id=employee_id)

        if name is not None:
            employee.name = name

        if dob is not None:
            employee.dob = dob

        if designation is not None:
            employee.designation = designation

        if department is not None:
            employee.department = department

        if campaigns_assigned is not None:
            employee.campaigns_assigned = campaigns_assigned

        if leads_generated is not None:
            employee.leads_generated = leads_generated

        if manager_ref is not None:
            employee.manager_ref_id = manager_ref

        if lead_permission_id is not None:
            employee.lead_permission_id = lead_permission_id

        if property_permission_id is not None:
            employee.property_permission_id = property_permission_id

        employee.save()
        return employee.employee_id_id

    @staticmethod
    def remove(employee_id: int) -> None:
        MarketingEmployee.objects.get(employee_id=employee_id).delete()

    @staticmethod
    def get(employee_id: int) -> dict:
        return MarketingEmployee.objects.filter(employee_id=employee_id).values(
            "employee_id", "name", "dob", "designation", "department",
            "campaigns_assigned", "leads_generated", "manager_ref_id",
            "lead_permission__permission_id", "property_permission__permission_id",
            "lead_permission__lead","property_permission__property",
            "created_date_time", "employee_id__phone_number", "employee_id__email"
        ).first()

    @staticmethod
    def get_all(
        sort_by: str = '',
        sort_order: str = '',
        filter_key: str = '',
        filter_value: str = '',
        search_key: str = '',
    ) -> list:
        data = MarketingEmployee.objects.all()
        if filter_key and filter_value:
            data = MarketingEmployee.objects.filter(
                **{f"{filter_key}__icontains": filter_value})
        if search_key:
            data = MarketingEmployee.objects.filter(
                Q(name__icontains=search_key) |
                Q(designation__icontains=search_key) |
                Q(department__icontains=search_key)
            )
        if sort_by:
            data = data.order_by(
                ('-' if sort_order == 'desc' else '') + sort_by)
        return list(
            data.values(
                 "employee_id", "name", "dob", "designation", "department",
            "campaigns_assigned", "leads_generated", "manager_ref_id",
            "lead_permission__permission_id", "property_permission__permission_id",
            "lead_permission__lead","property_permission__property",
            "created_date_time", "employee_id__phone_number", "employee_id__email"
            )
        )
