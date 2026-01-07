from django.db import models
from django.utils import timezone
from django.db.models import Q
from pms_apps.authentication.models import User


class Owner(models.Model):
    owner_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="owner_profile")
    name = models.CharField(max_length=100, default="")
    dob = models.DateField(null=True, blank=True)
    ownership_type = models.CharField(max_length=100, blank=True, null=True)
    properties_owned = models.IntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "owner"

    def __str__(self):
        return f"{self.name} ({self.owner_id.phone_number})"

    def create(
        self,
        owner_id: int,
        name: str,
        dob: str,
        ownership_type: str,
        properties_owned: int
    ) -> int:
        self.owner_id_id = owner_id
        self.name = name
        self.dob = dob
        self.ownership_type = ownership_type
        self.properties_owned = properties_owned
        self.save()
        return self.owner_id_id

    @staticmethod
    def update(
        owner_id: int,
        name: str,
        dob: str,
        ownership_type: str,
        properties_owned: int
    ) -> int:
        owner = Owner.objects.get(owner_id=owner_id)
        owner.name = name
        owner.dob = dob
        owner.ownership_type = ownership_type
        owner.properties_owned = properties_owned
        owner.save()
        return owner.owner_id_id

    @staticmethod
    def remove(owner_id: int) -> None:
        Owner.objects.get(owner_id=owner_id).delete()

    @staticmethod
    def get(owner_id: int) -> dict:
        return Owner.objects.filter(owner_id=owner_id).values(
            "owner_id", "name", "dob", "ownership_type", "properties_owned",
            "created_date_time", "owner_id__phone_number", "owner_id__email"
        ).first()

    @staticmethod
    def get_all(
        sort_by: str = '',
        sort_order: str = '',
        filter_key: str = '',
        filter_value: str = '',
        search_key: str = '',
    ) -> list:
        data = Owner.objects.all()
        if filter_key and filter_value:
            data = Owner.objects.filter(
                **{f"{filter_key}__icontains": filter_value})
        if search_key:
            data = Owner.objects.filter(
                Q(name__icontains=search_key) |
                Q(ownership_type__icontains=search_key)
            )
        if sort_by:
            data = data.order_by(
                ('-' if sort_order == 'desc' else '') + sort_by)
        return list(
            data.values(
                "owner_id", "name", "dob", "ownership_type", "properties_owned",
                "created_date_time", "owner_id__phone_number", "owner_id__email"
            )
        )
