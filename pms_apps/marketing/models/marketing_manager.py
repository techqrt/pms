from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User
from pms_apps.common.models.permissions import LeadPermission, PropertyPermission


class MarketingManager(models.Model):
    manager_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="marketing_manager_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    campaigns_led = models.IntegerField(default=0)
    team_size = models.IntegerField(default=0)

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
        db_table = "marketing_manager"

    def __str__(self):
        return f"{self.name} ({self.manager_id.phone_number})"


    @staticmethod
    def get_permissions(user_id: int) -> dict:
        manager = MarketingManager.objects.filter(manager_id__user_id=user_id).first()

        permissions = {}
        if manager:
            if manager.lead_permission:
                permissions["lead"] = manager.lead_permission.lead
            if manager.property_permission:
                permissions["property"] = manager.property_permission.property

        return {"permissions": permissions}

 
    def create(
        self,
        manager_id: int,
        name: str,
        dob: str,
        department: str,
        campaigns_led: int,
        team_size: int,
        lead_permission_id: int = None,
        property_permission_id: int = None,
    ) -> int:
        self.manager_id_id = manager_id
        self.name = name
        self.dob = dob
        self.department = department
        self.campaigns_led = campaigns_led
        self.team_size = team_size
        self.lead_permission = LeadPermission(lead_permission_id)
        self.property_permission = PropertyPermission(property_permission_id)

        self.created_date_time = timezone.now()
        self.save()
        return self.manager_id_id

    @staticmethod
    def update(
        manager_id: int = None,
        name: str = None,
        dob: str = None,
        department: str = None,
        campaigns_led: int = None,
        team_size: int = None,
        lead_permission_id: int = None,
        property_permission_id: int = None,
    ) -> int:
        manager = MarketingManager.objects.get(manager_id=manager_id)

        if name is not None:
            manager.name = name

        if dob is not None:
            manager.dob = dob

        if department is not None:
            manager.department = department

        if campaigns_led is not None:
            manager.campaigns_led = campaigns_led

        if team_size is not None:
            manager.team_size = team_size

        if lead_permission_id is not None:
            manager.lead_permission_id = lead_permission_id

        if property_permission_id is not None:
            manager.property_permission_id = property_permission_id

        manager.save()
        return manager.manager_id_id


    @staticmethod
    def remove(manager_id: int) -> None:
        MarketingManager.objects.get(manager_id_id=manager_id).delete()


    @staticmethod
    def get(manager_id: int) -> dict:
        return MarketingManager.objects.filter(manager_id__user_id=manager_id).values(
            "manager_id",
            "name",
            "dob",
            "department",
            "campaigns_led",
            "team_size",
            "created_date_time",
            "property_permission__permission_id",
            "property_permission__property",
            "lead_permission__permission_id",
            "lead_permission__lead",
            "manager_id__phone_number",
            "manager_id__email",
        ).first()

    @staticmethod
    def get_all(
        sort_by: str = '',
        sort_order: str = '',
        filter_key: str = '',
        filter_value: str = '',
        search_key: str = '',
    ) -> list:
        data = MarketingManager.objects.all()

        if filter_key and filter_value:
            data = data.filter(**{f"{filter_key}__icontains": filter_value})

        if search_key:
            data = data.filter(
                Q(name__icontains=search_key) |
                Q(department__icontains=search_key)
            )

        if sort_by:
            data = data.order_by(
                ('-' if sort_order == 'desc' else '') + sort_by
            )

        return list(
            data.values(
                 "manager_id",
                    "name",
                    "dob",
                    "department",
                    "campaigns_led",
                    "team_size",
                    "created_date_time",
                    "property_permission__permission_id",
                    "property_permission__property",
                    "lead_permission__permission_id",
                    "lead_permission__lead",
                    "manager_id__phone_number",
                    "manager_id__email",
            )
        )
