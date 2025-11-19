from django.db import models

class PropertyPermission(models.Model):
    permission_id = models.AutoField(
        primary_key=True,
        verbose_name="Lead Permission Id"
    )
    property = models.BooleanField(
        verbose_name="Is Property Permitted",
        default=False
    )

    class Meta:
        db_table = "lead_permission"

    def __str__(self):
        return f"Permission ID: {self.permission_id} (Property: {self.property})"

    def create(self,property: bool) -> int:
        self.property = property
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, property: bool) -> int:

        permission = PropertyPermission.objects.get(permission_id=permission_id)
        permission.property = property
        permission.save()
        return permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        PropertyPermission.objects.get(permission_id=permission_id).delete()