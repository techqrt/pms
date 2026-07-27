from django.db import models


class CheckOutDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ("Tenant ID Proof", "Tenant ID Proof"),
        ("Passport Copy", "Passport Copy"),
        ("Agreement Copy", "Agreement Copy"),
        ("Inspection Photo", "Inspection Photo"),
        ("Meter Reading Photo", "Meter Reading Photo"),
        ("Key Return Photo", "Key Return Photo"),
        ("Repair Document", "Repair Document"),
        ("Notice", "Notice"),
        ("Other", "Other"),
    ]

    IMAGE_ONLY_DOCUMENT_TYPES = {"Inspection Photo", "Meter Reading Photo"}

    CATEGORY_BY_TYPE = {
        "Tenant ID Proof": "Tenant",
        "Passport Copy": "Tenant",
        "Agreement Copy": "Agreement",
        "Inspection Photo": "Inspection",
        "Meter Reading Photo": "Utility",
        "Key Return Photo": "Key Return",
        "Repair Document": "Repair",
        "Notice": "Notice",
        "Other": "Other",
    }

    check_out_document_id = models.AutoField(primary_key=True)
    check_out = models.ForeignKey(
        "checkin_checkout.CheckOut",
        on_delete=models.CASCADE,
        related_name="documents"
    )
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    document_name = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to="checkin_checkout/check_out_documents/", max_length=500)
    linked_to_label = models.CharField(max_length=255, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_out_documents_uploaded"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "check_out_document"
        ordering = ["-created_at"]
        verbose_name = "Check-Out Document"
        verbose_name_plural = "Check-Out Documents"

    def __str__(self):
        return f"{self.document_type} for CheckOut {self.check_out_id}"
