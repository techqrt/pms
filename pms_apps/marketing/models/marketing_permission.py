from django.db import models
from django.utils import timezone


class MarketingPermission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    lead = models.BooleanField(null=True, blank=True)
    property = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = "marketing_permission"

    def __str__(self):
        return f"{self.lead} {self.property}"

    # ----------------------
    # Static CRUD Operations
    # ----------------------

    def create(self, lead: bool, property: bool) -> int:
        self.lead = lead
        self.property = property
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, lead: bool, property: bool) -> int:
        permission = MarketingPermission.objects.get(permission_id=permission_id)
        permission.lead = lead
        permission.property = property
        permission.save()
        return permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        MarketingPermission.objects.get(permission_id=permission_id).delete()
