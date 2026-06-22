from django.db import models


class CheckOut(models.Model):
    CHECK_OUT_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Inspection Pending", "Inspection Pending"),
        ("Approved", "Approved"),
        ("Active", "Active"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    TENANT_TYPE_CHOICES = [
        ("Individual", "Individual"),
        ("Corporate", "Corporate"),
    ]

    YES_NO_CHOICES = [
        ("Yes", "Yes"),
        ("No", "No"),
    ]

    PAYMENT_MODE_CHOICES = [
        ("Cash", "Cash"),
        ("Bank Transfer", "Bank Transfer"),
        ("Online", "Online"),
        ("Cheque", "Cheque"),
    ]

    APPROVAL_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    CHARGE_TYPE_CHOICES = [
        ("Security Deposit Refund", "Security Deposit Refund"),
        ("Deduction", "Deduction"),
        ("Pending Dues", "Pending Dues"),
        ("Other", "Other"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Partially Paid", "Partially Paid"),
        ("Refunded", "Refunded"),
    ]

    KEY_RETURN_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Returned", "Returned"),
        ("Not Returned", "Not Returned"),
        ("Lost", "Lost"),
    ]

    check_out_id = models.AutoField(primary_key=True)

    # Core Relations
    property = models.ForeignKey(
        "property.Property",
        on_delete=models.CASCADE,
        related_name="check_outs"
    )
    property_assignment = models.ForeignKey(
        "property.PropertyAssignment",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_outs"
    )
    check_in = models.ForeignKey(
        "checkin_checkout.CheckIn",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_outs"
    )
    tenant = models.ForeignKey(
        "lead.Lead",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_outs"
    )
    assigned_employee = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_outs_assigned"
    )

    # A. Check-Out Information
    check_out_code = models.CharField(max_length=50, unique=True)
    check_out_date = models.DateField(null=True, blank=True)
    check_out_status = models.CharField(
        max_length=30,
        choices=CHECK_OUT_STATUS_CHOICES,
        default="Pending"
    )
    remarks_notes = models.TextField(blank=True, default="")

    # B. Tenant Details (snapshot)
    tenant_code = models.CharField(max_length=50, null=True, blank=True)
    tenant_name = models.CharField(max_length=255, null=True, blank=True)
    tenant_type = models.CharField(
        max_length=20,
        choices=TENANT_TYPE_CHOICES,
        null=True,
        blank=True
    )
    tenant_mobile_number = models.CharField(max_length=20, null=True, blank=True)
    tenant_email = models.EmailField(null=True, blank=True)
    tenant_civil_id = models.CharField(max_length=50, null=True, blank=True)
    tenant_passport_number = models.CharField(max_length=50, null=True, blank=True)
    tenant_nationality = models.CharField(max_length=100, null=True, blank=True)

    # C. Property Details (snapshot)
    property_type = models.CharField(max_length=100, null=True, blank=True)
    property_code = models.CharField(max_length=100, null=True, blank=True)
    building_name = models.CharField(max_length=150, null=True, blank=True)
    flat_unit_number = models.CharField(max_length=50, null=True, blank=True)
    floor_number = models.CharField(max_length=50, null=True, blank=True)
    property_status = models.CharField(max_length=50, null=True, blank=True)

    # D. Rental Details
    monthly_rent = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    security_deposit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    advance_rent_received = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    first_month_rent_paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE_CHOICES,
        null=True,
        blank=True
    )
    maintenance_charges = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # E. Property Inspection
    inspection_required = models.CharField(
        max_length=10,
        choices=YES_NO_CHOICES,
        null=True,
        blank=True
    )
    inspection_date = models.DateField(null=True, blank=True)
    technician_type = models.CharField(max_length=100, null=True, blank=True)
    manager_approval = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        null=True,
        blank=True
    )
    issue_identified = models.TextField(blank=True, default="")
    supervisor_remarks = models.TextField(blank=True, default="")

    # F. Repair & Damage
    repair_required = models.CharField(
        max_length=10,
        choices=YES_NO_CHOICES,
        null=True,
        blank=True
    )
    quotation_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    inventory_available = models.CharField(
        max_length=10,
        choices=YES_NO_CHOICES,
        null=True,
        blank=True
    )
    gm_approval = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        null=True,
        blank=True
    )
    landlord_consent = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        null=True,
        blank=True
    )
    finance_alert_generated = models.CharField(
        max_length=10,
        choices=YES_NO_CHOICES,
        null=True,
        blank=True
    )
    rent_adjustment_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # G. Check-Out Utility Meter Readings
    electricity_meter_reading = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    water_meter_reading = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    gas_meter_reading = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # H. Finance Details
    charge_type = models.CharField(
        max_length=50,
        choices=CHARGE_TYPE_CHOICES,
        null=True,
        blank=True
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        null=True,
        blank=True
    )
    payment_date = models.DateField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    payment_proof = models.FileField(
        upload_to="checkin_checkout/payment_proofs/",
        max_length=500,
        null=True,
        blank=True
    )

    # I. Key Return
    key_number = models.CharField(max_length=100, null=True, blank=True)
    key_return = models.CharField(
        max_length=10,
        choices=YES_NO_CHOICES,
        null=True,
        blank=True
    )
    expected_return_date = models.DateField(null=True, blank=True)
    confirmation_received = models.CharField(
        max_length=10,
        choices=YES_NO_CHOICES,
        null=True,
        blank=True
    )
    key_return_date = models.DateField(null=True, blank=True)
    key_return_status = models.CharField(
        max_length=20,
        choices=KEY_RETURN_STATUS_CHOICES,
        default="Pending"
    )

    # J. Documents Upload
    # Stored via the related `CheckOutDocument` model (see check_out_document.py),
    # accessible through the `documents` related_name.

    # K. Comments
    internal_comments = models.TextField(blank=True, default="")
    tenant_remarks = models.TextField(blank=True, default="")
    special_instructions = models.TextField(blank=True, default="")

    # L. System Fields
    created_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_outs_created"
    )
    updated_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_outs_updated"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_history = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "check_out"
        ordering = ["-created_at"]
        verbose_name = "Check-Out"
        verbose_name_plural = "Check-Outs"

    def __str__(self):
        return f"CheckOut {self.check_out_code} - Property {self.property_id}"
