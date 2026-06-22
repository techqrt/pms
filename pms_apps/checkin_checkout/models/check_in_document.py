from django.db import models


class CheckInDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ("Tenant ID Proof", "Tenant ID Proof"),
        ("Passport Copy", "Passport Copy"),
        ("Agreement Copy", "Agreement Copy"),
        ("Inspection Photo", "Inspection Photo"),
        ("Meter Reading Photo", "Meter Reading Photo"),
        ("Company Seal", "Company Seal"),
        ("Key Handover Photo", "Key Handover Photo"),
        ("Key Receipt", "Key Receipt"),
        ("Rent Invoice", "Rent Invoice"),
        ("NOC Certificate", "NOC Certificate"),
        ("Property Photo", "Property Photo"),
        ("Move-In Checklist", "Move-In Checklist"),
        ("Insurance Document", "Insurance Document"),
        ("Stamp Duty", "Stamp Duty"),
        ("Address Proof", "Address Proof"),
        ("Police Clearance", "Police Clearance"),
        ("Agreement Signed", "Agreement Signed"),
    ]

    # Category grouping for the Documents tab — derived from document_type, not stored.
    CATEGORY_BY_TYPE = {
        "Tenant ID Proof": "Tenant",
        "Passport Copy": "Tenant",
        "Address Proof": "Tenant",
        "Police Clearance": "Tenant",
        "Agreement Copy": "Agreement",
        "Company Seal": "Agreement",
        "Agreement Signed": "Agreement",
        "Inspection Photo": "Inspection",
        "Move-In Checklist": "Inspection",
        "Meter Reading Photo": "Property",
        "Property Photo": "Property",
        "Key Handover Photo": "Key Handover",
        "Key Receipt": "Key Handover",
        "Rent Invoice": "Finance",
        "NOC Certificate": "Compliance",
        "Insurance Document": "Compliance",
        "Stamp Duty": "Compliance",
    }

    check_in_document_id = models.AutoField(primary_key=True)
    check_in = models.ForeignKey(
        "checkin_checkout.CheckIn",
        on_delete=models.CASCADE,
        related_name="documents"
    )
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to="checkin_checkout/check_in_documents/", max_length=500)
    linked_to_label = models.CharField(max_length=255, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_in_documents_uploaded"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "check_in_document"
        ordering = ["-created_at"]
        verbose_name = "Check-In Document"
        verbose_name_plural = "Check-In Documents"

    def __str__(self):
        return f"{self.document_type} for CheckIn {self.check_in_id}"
