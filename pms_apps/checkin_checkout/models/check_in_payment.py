from django.db import models


class CheckInPayment(models.Model):
    STATUS_CHOICES = [
        ("Paid", "Paid"),
        ("Pending", "Pending"),
    ]

    check_in_payment_id = models.AutoField(primary_key=True)
    check_in = models.ForeignKey(
        "checkin_checkout.CheckIn",
        on_delete=models.CASCADE,
        related_name="payments"
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    payment_date = models.DateField(null=True, blank=True)
    receipt_ref_no = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(blank=True, default="")
    created_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_in_payments_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "check_in_payment"
        ordering = ["-created_at"]
        verbose_name = "Check-In Payment"
        verbose_name_plural = "Check-In Payments"

    def __str__(self):
        return f"{self.description} ({self.amount}) for CheckIn {self.check_in_id}"

    def create(
        self,
        check_in_id: int,
        description: str,
        amount,
        status: str = "Pending",
        payment_date=None,
        receipt_ref_no: str = None,
        remarks: str = "",
        created_by: int = None,
    ) -> int:
        self.check_in_id = check_in_id
        self.description = description
        self.amount = amount
        self.status = status
        self.payment_date = payment_date
        self.receipt_ref_no = receipt_ref_no
        self.remarks = remarks
        self.created_by_id = created_by
        self.save()
        return self.check_in_payment_id

    @staticmethod
    def get_all_for_check_in(check_in_id: int):
        return CheckInPayment.objects.filter(
            check_in_id=check_in_id, is_active=True
        ).values(
            "check_in_payment_id", "description", "amount", "status",
            "payment_date", "receipt_ref_no", "remarks", "created_at",
        )

    @staticmethod
    def update(
        check_in_payment_id: int,
        description: str = None,
        amount=None,
        status: str = None,
        payment_date=None,
        receipt_ref_no: str = None,
        remarks: str = None,
        updated_by: int = None,
    ) -> int:
        try:
            payment = CheckInPayment.objects.get(check_in_payment_id=check_in_payment_id)
        except CheckInPayment.DoesNotExist:
            raise ValueError(f"Invalid Check-In Payment Id: {check_in_payment_id}")

        if description is not None:
            payment.description = description
        if amount is not None:
            payment.amount = amount
        if status is not None:
            payment.status = status
        if payment_date is not None:
            payment.payment_date = payment_date
        if receipt_ref_no is not None:
            payment.receipt_ref_no = receipt_ref_no
        if remarks is not None:
            payment.remarks = remarks

        payment.save()
        return payment.check_in_payment_id

    @staticmethod
    def delete(check_in_payment_id: int) -> None:
        CheckInPayment.objects.filter(
            check_in_payment_id=check_in_payment_id
        ).update(is_active=False)
