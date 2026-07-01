from django.db import models


class CheckOutKey(models.Model):
    STATUS_CHOICES = [
        ("Returned", "Returned"),
        ("Pending", "Pending"),
    ]

    check_out_key_id = models.AutoField(primary_key=True)
    check_out = models.ForeignKey(
        "checkin_checkout.CheckOut",
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
        related_name="check_out_keys_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "check_out_key"
        ordering = ["check_out_key_id"]
        verbose_name = "Check-Out Key"
        verbose_name_plural = "Check-Out Keys"

    def __str__(self):
        return f"{self.key_number} ({self.key_type}) for CheckOut {self.check_out_id}"

    def create(
        self,
        check_out_id: int,
        key_number: str,
        key_type: str,
        status: str = "Pending",
        remarks: str = "",
        created_by: int = None,
    ) -> int:
        self.check_out_id = check_out_id
        self.key_number = key_number
        self.key_type = key_type
        self.status = status
        self.remarks = remarks
        self.created_by_id = created_by
        self.save()
        return self.check_out_key_id

    @staticmethod
    def get_all_for_check_out(check_out_id: int):
        return CheckOutKey.objects.filter(
            check_out_id=check_out_id, is_active=True
        ).values(
            "check_out_key_id", "key_number", "key_type", "status", "remarks", "created_at",
        )

    @staticmethod
    def update(
        check_out_key_id: int,
        key_number: str = None,
        key_type: str = None,
        status: str = None,
        remarks: str = None,
        updated_by: int = None,
    ) -> int:
        try:
            key = CheckOutKey.objects.get(check_out_key_id=check_out_key_id)
        except CheckOutKey.DoesNotExist:
            raise ValueError(f"Invalid Check-Out Key Id: {check_out_key_id}")

        if key_number is not None:
            key.key_number = key_number
        if key_type is not None:
            key.key_type = key_type
        if status is not None:
            key.status = status
        if remarks is not None:
            key.remarks = remarks

        key.save()
        return key.check_out_key_id

    @staticmethod
    def delete(check_out_key_id: int) -> None:
        CheckOutKey.objects.filter(
            check_out_key_id=check_out_key_id
        ).update(is_active=False)
