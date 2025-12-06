from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User
from pms_apps.marketing.models.marketing_permission import MarketingPermission


class MarketingManager(models.Model):
    manager_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="marketing_manager_profile"
    )
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    # e.g. Digital, Field Marketing
    department = models.CharField(max_length=100, blank=True, null=True)
    campaigns_led = models.IntegerField(default=0)
    team_size = models.IntegerField(default=0)
    permission = models.ForeignKey(
        MarketingPermission, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="marketing_manager_permission"
    )
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "marketing_manager"

    def __str__(self):
        return f"{self.name} {self.manager_id.phone_number}"

    # ----------------------
    # Static CRUD Operations
    # ----------------------

    def create(
        self,
        manager_id: int,
        name: str,
        dob: str,
        department: str,
        campaigns_led: int,
        team_size: int,
        permission_id: int,
    ) -> int:
        """Create a new Marketing Manager profile"""
        self.manager_id_id = manager_id
        self.name = name
        self.dob = dob
        self.department = department
        self.campaigns_led = campaigns_led
        self.team_size = team_size
        if permission_id:
            self.permission_id = permission_id
        self.created_date_time = timezone.now()
        self.save()
        return self.manager_id_id

    @staticmethod
    def update(
        manager_id: int,
        name: str,
        dob: str,
        department: str,
        campaigns_led: int,
        team_size: int,
        permission_id: int,
    ) -> int:
        """Update marketing manager profile"""
        manager = MarketingManager.objects.get(manager_id=manager_id)
        manager.name = name
        manager.dob = dob
        manager.department = department
        manager.campaigns_led = campaigns_led
        manager.team_size = team_size
        if permission_id:
            manager.permission_id = permission_id
        manager.save()
        return manager.manager_id_id

    @staticmethod
    def remove(manager_id: int) -> None:
        """Delete marketing manager profile"""
        MarketingManager.objects.get(manager_id=manager_id).delete()

    @staticmethod
    def get(manager_id: int) -> dict:
        """Fetch single marketing manager profile"""
        return MarketingManager.objects.filter(manager_id=manager_id).values(
            "manager_id", "name", "dob", "department", "campaigns_led", "team_size",
            "permission_id", "permission_id__lead", "permission_id__property",
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
        """Fetch all marketing managers"""
        data = MarketingManager.objects.all()
        if filter_key and filter_value:
            data = MarketingManager.objects.filter(
                **{f"{filter_key}__icontains": filter_value})
        if search_key:
            data = MarketingManager.objects.filter(
                Q(name__icontains=search_key) |
                Q(department__icontains=search_key)
            )
        if sort_by:
            data = data.order_by(
                ('-' if sort_order == 'desc' else '') + sort_by)
        return list(
            data.values(
                "manager_id", "manager_id__phone_number", "manager_id__email",
                "name", "dob", "department", "campaigns_led", "team_size",
                "permission_id", "permission_id__lead", "permission_id__property",
                "created_date_time"
            )
        )
