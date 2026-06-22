from django.db import models


class CheckInKey(models.Model):
    STATUS_CHOICES = [
        ("Handovered", "Handovered"),
        ("Pending", "Pending"),
    ]

    check_in_key_id = models.AutoField(primary_key=True)
    check_in = models.ForeignKey(
        "checkin_checkout.CheckIn",
        on_delete=models.CASCADE,
        related_name="keys"
    )
    key_number = models.CharField(max_length=100)
    key_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    remarks = models.TextField(blank=True, default="")
    created_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_in_keys_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "check_in_key"
        ordering = ["check_in_key_id"]
        verbose_name = "Check-In Key"
        verbose_name_plural = "Check-In Keys"

    def __str__(self):
        return f"{self.key_number} ({self.key_type}) for CheckIn {self.check_in_id}"

    def create(
        self,
        check_in_id: int,
        key_number: str,
        key_type: str,
        status: str = "Pending",
        remarks: str = "",
        created_by: int = None,
    ) -> int:
        self.check_in_id = check_in_id
        self.key_number = key_number
        self.key_type = key_type
        self.status = status
        self.remarks = remarks
        self.created_by_id = created_by
        self.save()
        return self.check_in_key_id

    @staticmethod
    def get_all_for_check_in(check_in_id: int):
        return CheckInKey.objects.filter(
            check_in_id=check_in_id, is_active=True
        ).values(
            "check_in_key_id", "key_number", "key_type", "status", "remarks", "created_at",
        )

    @staticmethod
    def update(
        check_in_key_id: int,
        key_number: str = None,
        key_type: str = None,
        status: str = None,
        remarks: str = None,
        updated_by: int = None,
    ) -> int:
        try:
            key = CheckInKey.objects.get(check_in_key_id=check_in_key_id)
        except CheckInKey.DoesNotExist:
            raise ValueError(f"Invalid Check-In Key Id: {check_in_key_id}")

        if key_number is not None:
            key.key_number = key_number
        if key_type is not None:
            key.key_type = key_type
        if status is not None:
            key.status = status
        if remarks is not None:
            key.remarks = remarks

        key.save()
        return key.check_in_key_id

    @staticmethod
    def delete(check_in_key_id: int) -> None:
        CheckInKey.objects.filter(
            check_in_key_id=check_in_key_id
        ).update(is_active=False)
