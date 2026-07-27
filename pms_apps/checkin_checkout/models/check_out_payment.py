from django.db import models


class CheckOutPayment(models.Model):
    STATUS_CHOICES = [
        ("Paid", "Paid"),
        ("Pending", "Pending"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("Cash", "Cash"),
        ("Bank Transfer", "Bank Transfer"),
        ("Online", "Online"),
        ("Cheque", "Cheque"),
    ]

    check_out_payment_id = models.AutoField(primary_key=True)
    check_out = models.ForeignKey(
        "checkin_checkout.CheckOut",
        on_delete=models.CASCADE,
        related_name="payments"
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    receipt_ref_no = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(blank=True, default="")
    created_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_out_payments_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "check_out_payment"
        ordering = ["-created_at"]
        verbose_name = "Check-Out Payment"
        verbose_name_plural = "Check-Out Payments"

    def __str__(self):
        return f"{self.description} ({self.amount}) for CheckOut {self.check_out_id}"

    def create(
        self,
        check_out_id: int,
        description: str,
        amount,
        tax=None,
        status: str = "Pending",
        payment_method: str = None,
        payment_date=None,
        receipt_ref_no: str = None,
        remarks: str = "",
        created_by: int = None,
    ) -> int:
        self.check_out_id = check_out_id
        self.description = description
        self.amount = amount
        self.tax = tax
        self.status = status
        self.payment_method = payment_method
        self.payment_date = payment_date
        self.receipt_ref_no = receipt_ref_no
        self.remarks = remarks
        self.created_by_id = created_by
        self.save()
        return self.check_out_payment_id

    @staticmethod
    def get_all_for_check_out(check_out_id: int):
        return CheckOutPayment.objects.filter(
            check_out_id=check_out_id, is_active=True
        ).values(
            "check_out_payment_id", "description", "amount", "tax", "status", "payment_method",
            "payment_date", "receipt_ref_no", "remarks", "created_at",
            "created_by_id", "created_by__name",
        )

    @staticmethod
    def update(
        check_out_payment_id: int,
        description: str = None,
        amount=None,
        tax=None,
        status: str = None,
        payment_method: str = None,
        payment_date=None,
        receipt_ref_no: str = None,
        remarks: str = None,
        updated_by: int = None,
    ) -> int:
        try:
            payment = CheckOutPayment.objects.get(check_out_payment_id=check_out_payment_id)
        except CheckOutPayment.DoesNotExist:
            raise ValueError(f"Invalid Check-Out Payment Id: {check_out_payment_id}")

        if description is not None:
            payment.description = description
        if amount is not None:
            payment.amount = amount
        if tax is not None:
            payment.tax = tax
        if status is not None:
            payment.status = status
        if payment_method is not None:
            payment.payment_method = payment_method
        if payment_date is not None:
            payment.payment_date = payment_date
        if receipt_ref_no is not None:
            payment.receipt_ref_no = receipt_ref_no
        if remarks is not None:
            payment.remarks = remarks

        payment.save()
        return payment.check_out_payment_id

    @staticmethod
    def delete(check_out_payment_id: int) -> None:
        CheckOutPayment.objects.filter(
            check_out_payment_id=check_out_payment_id
        ).update(is_active=False)
