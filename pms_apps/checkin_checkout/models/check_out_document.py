from django.db import models


class CheckOutDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ("Tenant ID Proof", "Tenant ID Proof"),
        ("Passport Copy", "Passport Copy"),
        ("Address Proof", "Address Proof"),
        ("Police Clearance", "Police Clearance"),
        ("Agreement Copy", "Agreement Copy"),
        ("Agreement Signed", "Agreement Signed"),
        ("Company Seal", "Company Seal"),
        ("Inspection Photo", "Inspection Photo"),
        ("Meter Reading Photo", "Meter Reading Photo"),
        ("Property Photo", "Property Photo"),
        ("Key Return Photo", "Key Return Photo"),
        ("Repair Document", "Repair Document"),
        ("Rent Invoice", "Rent Invoice"),
        ("NOC Certificate", "NOC Certificate"),
        ("Insurance Document", "Insurance Document"),
        ("Stamp Duty", "Stamp Duty"),
        ("Notice", "Notice"),
        ("Other", "Other"),
    ]

    IMAGE_ONLY_DOCUMENT_TYPES = {"Inspection Photo", "Meter Reading Photo", "Key Return Photo"}

    CATEGORY_BY_TYPE = {
        "Tenant ID Proof": "Tenant",
        "Passport Copy": "Tenant",
        "Address Proof": "Tenant",
        "Police Clearance": "Tenant",
        "Agreement Copy": "Agreement",
        "Agreement Signed": "Agreement",
        "Company Seal": "Agreement",
        "Inspection Photo": "Inspection",
        "Meter Reading Photo": "Utility",
        "Property Photo": "Property",
        "Key Return Photo": "Key Return",
        "Repair Document": "Repair",
        "Rent Invoice": "Finance",
        "NOC Certificate": "Compliance",
        "Insurance Document": "Compliance",
        "Stamp Duty": "Compliance",
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

    @staticmethod
    def update(
        check_out_document_id: int,
        document_name: str = None,
        linked_to_label: str = None,
        expiry_date=None,
        updated_by: int = None,
    ) -> int:
        try:
            document = CheckOutDocument.objects.get(check_out_document_id=check_out_document_id)
        except CheckOutDocument.DoesNotExist:
            raise ValueError(f"Invalid Check-Out Document Id: {check_out_document_id}")

        if document_name is not None:
            document.document_name = document_name
        if linked_to_label is not None:
            document.linked_to_label = linked_to_label
        if expiry_date is not None:
            document.expiry_date = expiry_date

        document.save()
        return document.check_out_document_id

    @staticmethod
    def delete(check_out_document_id: int) -> None:
        CheckOutDocument.objects.filter(
            check_out_document_id=check_out_document_id
        ).update(is_active=False)
