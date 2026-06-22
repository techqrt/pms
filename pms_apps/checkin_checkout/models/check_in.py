from django.db import models


class CheckIn(models.Model):
    CHECK_IN_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Key Pending", "Key Pending"),
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

    AGREEMENT_TYPE_CHOICES = [
        ("Government Agreement", "Government Agreement"),
        ("Internal Agreement", "Internal Agreement"),
    ]

    AGREEMENT_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Prepared", "Prepared"),
        ("Signed", "Signed"),
        ("Executed", "Executed"),
        ("Terminated", "Terminated"),
    ]

    KEY_HANDOVER_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Booked", "Booked"),
        ("Handed Over", "Handed Over"),
        ("Returned", "Returned"),
    ]

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    MARITAL_STATUS_CHOICES = [
        ("Single", "Single"),
        ("Married", "Married"),
        ("Divorced", "Divorced"),
        ("Widowed", "Widowed"),
    ]

    INSPECTION_TYPE_CHOICES = [
        ("Move-In Inspection", "Move-In Inspection"),
        ("Move-Out Inspection", "Move-Out Inspection"),
        ("Periodic Inspection", "Periodic Inspection"),
    ]

    PRIORITY_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    check_in_id = models.AutoField(primary_key=True)

    # Core Relations
    property = models.ForeignKey(
        "property.Property",
        on_delete=models.CASCADE,
        related_name="check_ins"
    )
    property_assignment = models.ForeignKey(
        "property.PropertyAssignment",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_ins"
    )
    tenant = models.ForeignKey(
        "lead.Lead",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_ins"
    )
    assigned_employee = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_ins_assigned"
    )

    # A. Check-In Information
    check_in_code = models.CharField(max_length=50, unique=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_in_status = models.CharField(
        max_length=30,
        choices=CHECK_IN_STATUS_CHOICES,
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
    tenant_address = models.TextField(blank=True, default="")
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    alternate_mobile_number = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=20, null=True, blank=True)
    profession = models.CharField(max_length=150, null=True, blank=True)
    company_name = models.CharField(max_length=150, null=True, blank=True)
    move_in_reason = models.CharField(max_length=255, null=True, blank=True)
    number_of_occupants = models.PositiveIntegerField(null=True, blank=True)

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
    inspection_priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        null=True,
        blank=True
    )
    inspection_type = models.CharField(
        max_length=30,
        choices=INSPECTION_TYPE_CHOICES,
        null=True,
        blank=True
    )
    inspection_duration = models.CharField(max_length=20, null=True, blank=True)
    next_inspection_due = models.DateField(null=True, blank=True)

    # F. Repair & Approval
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
    repair_priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        null=True,
        blank=True
    )
    recommended_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_ins_recommended"
    )
    approved_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_ins_approved"
    )
    approved_on = models.DateField(null=True, blank=True)
    inspector_comments = models.TextField(blank=True, default="")

    # G. Utility Meter Readings
    electricity_meter_reading = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    water_meter_reading = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    gas_meter_reading = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    utility_adjustment_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # H. Agreement Details
    agreement_type = models.CharField(
        max_length=100,
        choices=AGREEMENT_TYPE_CHOICES,
        null=True,
        blank=True
    )
    agreement_status = models.CharField(
        max_length=20,
        choices=AGREEMENT_STATUS_CHOICES,
        default="Pending"
    )
    agreement_start_date = models.DateField(null=True, blank=True)
    agreement_end_date = models.DateField(null=True, blank=True)
    agreement_document = models.FileField(
        upload_to="checkin_checkout/agreement_documents/",
        max_length=500,
        null=True,
        blank=True
    )
    agreement_template = models.CharField(max_length=100, null=True, blank=True)
    agreement_number = models.CharField(max_length=50, null=True, blank=True)
    generated_on = models.DateTimeField(null=True, blank=True)
    generated_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_ins_agreement_generated"
    )
    submitted_to_tenant_on = models.DateTimeField(null=True, blank=True)
    tenant_signed_on = models.DateTimeField(null=True, blank=True)
    manager_signed_on = models.DateTimeField(null=True, blank=True)
    signed_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_ins_agreement_signed"
    )
    renewal_reminder_date = models.DateField(null=True, blank=True)
    auto_reminder_enabled = models.BooleanField(null=True, blank=True)
    agreement_notes = models.TextField(blank=True, default="")

    # I. Key Handover
    key_number = models.CharField(max_length=100, null=True, blank=True)
    key_type = models.CharField(max_length=100, null=True, blank=True)
    key_available = models.CharField(
        max_length=10,
        choices=YES_NO_CHOICES,
        null=True,
        blank=True
    )
    key_booking_date = models.DateField(null=True, blank=True)
    confirmation_received = models.CharField(
        max_length=10,
        choices=YES_NO_CHOICES,
        null=True,
        blank=True
    )
    key_delivery_date = models.DateField(null=True, blank=True)
    key_handover_status = models.CharField(
        max_length=20,
        choices=KEY_HANDOVER_STATUS_CHOICES,
        default="Pending"
    )
    expected_handover_date = models.DateTimeField(null=True, blank=True)
    handover_notes = models.TextField(blank=True, default="")
    tenant_confirmation_notes = models.TextField(blank=True, default="")
    key_booked_on = models.DateTimeField(null=True, blank=True)
    key_booked_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_ins_key_booked"
    )
    key_prepared_on = models.DateTimeField(null=True, blank=True)
    key_notified_on = models.DateTimeField(null=True, blank=True)
    handover_completed_on = models.DateTimeField(null=True, blank=True)
    handed_over_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_ins_key_handed_over"
    )

    # J. Documents Upload
    # Stored via the related `CheckInDocument` model (see check_in_document.py),
    # accessible through the `documents` related_name.

    # K. Comments
    internal_comments = models.TextField(blank=True, default="")
    tenant_remarks = models.TextField(blank=True, default="")
    special_instructions = models.TextField(blank=True, default="")

    # M. Activity Timeline (Overview tab)
    property_created_date = models.DateField(null=True, blank=True)
    listed_for_rent_date = models.DateField(null=True, blank=True)
    tenant_assigned_date = models.DateField(null=True, blank=True)
    assigned_to_employee_date = models.DateField(null=True, blank=True)
    property_occupied_date = models.DateField(null=True, blank=True)

    # L. System Fields
    created_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_ins_created"
    )
    updated_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_ins_updated"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_history = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "check_in"
        ordering = ["-created_at"]
        verbose_name = "Check-In"
        verbose_name_plural = "Check-Ins"

    def __str__(self):
        return f"CheckIn {self.check_in_code} - Property {self.property_id}"

    def create(
        self,
        property_id: int,
        created_by: int,
        property_assignment_id: int = None,
        tenant_id: int = None,
        assigned_employee_id: int = None,
        check_in_date=None,
        check_in_status: str = "Pending",
        remarks_notes: str = "",
        tenant_code: str = None,
        tenant_name: str = None,
        tenant_type: str = None,
        tenant_mobile_number: str = None,
        tenant_email: str = None,
        tenant_civil_id: str = None,
        tenant_passport_number: str = None,
        tenant_nationality: str = None,
        tenant_address: str = "",
        date_of_birth=None,
        gender: str = None,
        marital_status: str = None,
        alternate_mobile_number: str = None,
        emergency_contact_name: str = None,
        emergency_contact_number: str = None,
        profession: str = None,
        company_name: str = None,
        move_in_reason: str = None,
        number_of_occupants: int = None,
        property_type: str = None,
        property_code: str = None,
        building_name: str = None,
        flat_unit_number: str = None,
        floor_number: str = None,
        property_status: str = None,
        monthly_rent=None,
        security_deposit=None,
        advance_rent_received=None,
        first_month_rent_paid=None,
        payment_mode: str = None,
        maintenance_charges=None,
        inspection_required: str = None,
        inspection_date=None,
        technician_type: str = None,
        manager_approval: str = None,
        issue_identified: str = "",
        supervisor_remarks: str = "",
        inspection_priority: str = None,
        inspection_type: str = None,
        inspection_duration: str = None,
        next_inspection_due=None,
        repair_required: str = None,
        quotation_amount=None,
        inventory_available: str = None,
        gm_approval: str = None,
        landlord_consent: str = None,
        finance_alert_generated: str = None,
        rent_adjustment_amount=None,
        repair_priority: str = None,
        recommended_by_id: int = None,
        approved_by_id: int = None,
        approved_on=None,
        inspector_comments: str = "",
        electricity_meter_reading=None,
        water_meter_reading=None,
        gas_meter_reading=None,
        utility_adjustment_amount=None,
        agreement_type: str = None,
        agreement_status: str = "Pending",
        agreement_start_date=None,
        agreement_end_date=None,
        agreement_template: str = None,
        agreement_number: str = None,
        generated_on=None,
        generated_by_id: int = None,
        submitted_to_tenant_on=None,
        tenant_signed_on=None,
        manager_signed_on=None,
        signed_by_id: int = None,
        renewal_reminder_date=None,
        auto_reminder_enabled: bool = None,
        agreement_notes: str = "",
        key_number: str = None,
        key_type: str = None,
        key_available: str = None,
        key_booking_date=None,
        confirmation_received: str = None,
        key_delivery_date=None,
        key_handover_status: str = "Pending",
        expected_handover_date=None,
        handover_notes: str = "",
        tenant_confirmation_notes: str = "",
        key_booked_on=None,
        key_booked_by_id: int = None,
        key_prepared_on=None,
        key_notified_on=None,
        handover_completed_on=None,
        handed_over_by_id: int = None,
        internal_comments: str = "",
        tenant_remarks: str = "",
        special_instructions: str = "",
        property_created_date=None,
        listed_for_rent_date=None,
        tenant_assigned_date=None,
        assigned_to_employee_date=None,
        property_occupied_date=None,
    ) -> int:
        self.property_id = property_id
        self.property_assignment_id = property_assignment_id
        self.tenant_id = tenant_id
        self.assigned_employee_id = assigned_employee_id
        self.created_by_id = created_by

        # A. Check-In Information
        self.check_in_date = check_in_date
        self.check_in_status = check_in_status
        self.remarks_notes = remarks_notes

        # B. Tenant Details (snapshot)
        self.tenant_code = tenant_code
        self.tenant_name = tenant_name
        self.tenant_type = tenant_type
        self.tenant_mobile_number = tenant_mobile_number
        self.tenant_email = tenant_email
        self.tenant_civil_id = tenant_civil_id
        self.tenant_passport_number = tenant_passport_number
        self.tenant_nationality = tenant_nationality
        self.tenant_address = tenant_address
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.marital_status = marital_status
        self.alternate_mobile_number = alternate_mobile_number
        self.emergency_contact_name = emergency_contact_name
        self.emergency_contact_number = emergency_contact_number
        self.profession = profession
        self.company_name = company_name
        self.move_in_reason = move_in_reason
        self.number_of_occupants = number_of_occupants

        # C. Property Details (snapshot)
        self.property_type = property_type
        self.property_code = property_code
        self.building_name = building_name
        self.flat_unit_number = flat_unit_number
        self.floor_number = floor_number
        self.property_status = property_status

        # D. Rental Details
        self.monthly_rent = monthly_rent
        self.security_deposit = security_deposit
        self.advance_rent_received = advance_rent_received
        self.first_month_rent_paid = first_month_rent_paid
        self.payment_mode = payment_mode
        self.maintenance_charges = maintenance_charges

        # E. Property Inspection
        self.inspection_required = inspection_required
        self.inspection_date = inspection_date
        self.technician_type = technician_type
        self.manager_approval = manager_approval
        self.issue_identified = issue_identified
        self.supervisor_remarks = supervisor_remarks
        self.inspection_priority = inspection_priority
        self.inspection_type = inspection_type
        self.inspection_duration = inspection_duration
        self.next_inspection_due = next_inspection_due

        # F. Repair & Approval
        self.repair_required = repair_required
        self.quotation_amount = quotation_amount
        self.inventory_available = inventory_available
        self.gm_approval = gm_approval
        self.landlord_consent = landlord_consent
        self.finance_alert_generated = finance_alert_generated
        self.rent_adjustment_amount = rent_adjustment_amount
        self.repair_priority = repair_priority
        self.recommended_by_id = recommended_by_id
        self.approved_by_id = approved_by_id
        self.approved_on = approved_on
        self.inspector_comments = inspector_comments

        # G. Utility Meter Readings
        self.electricity_meter_reading = electricity_meter_reading
        self.water_meter_reading = water_meter_reading
        self.gas_meter_reading = gas_meter_reading
        self.utility_adjustment_amount = utility_adjustment_amount

        # H. Agreement Details
        self.agreement_type = agreement_type
        self.agreement_status = agreement_status
        self.agreement_start_date = agreement_start_date
        self.agreement_end_date = agreement_end_date
        self.agreement_template = agreement_template
        self.agreement_number = agreement_number
        self.generated_on = generated_on
        self.generated_by_id = generated_by_id
        self.submitted_to_tenant_on = submitted_to_tenant_on
        self.tenant_signed_on = tenant_signed_on
        self.manager_signed_on = manager_signed_on
        self.signed_by_id = signed_by_id
        self.renewal_reminder_date = renewal_reminder_date
        self.auto_reminder_enabled = auto_reminder_enabled
        self.agreement_notes = agreement_notes

        # I. Key Handover
        self.key_number = key_number
        self.key_type = key_type
        self.key_available = key_available
        self.key_booking_date = key_booking_date
        self.confirmation_received = confirmation_received
        self.key_delivery_date = key_delivery_date
        self.key_handover_status = key_handover_status
        self.expected_handover_date = expected_handover_date
        self.handover_notes = handover_notes
        self.tenant_confirmation_notes = tenant_confirmation_notes
        self.key_booked_on = key_booked_on
        self.key_booked_by_id = key_booked_by_id
        self.key_prepared_on = key_prepared_on
        self.key_notified_on = key_notified_on
        self.handover_completed_on = handover_completed_on
        self.handed_over_by_id = handed_over_by_id

        # K. Comments
        self.internal_comments = internal_comments
        self.tenant_remarks = tenant_remarks
        self.special_instructions = special_instructions

        # M. Activity Timeline
        self.property_created_date = property_created_date
        self.listed_for_rent_date = listed_for_rent_date
        self.tenant_assigned_date = tenant_assigned_date
        self.assigned_to_employee_date = assigned_to_employee_date
        self.property_occupied_date = property_occupied_date

        self.save()

        # Auto-generate the business code now that the primary key exists
        self.check_in_code = f"CHKIN-{self.check_in_id:06d}"
        self.status_history = f"Created -> {self.check_in_status}"
        self.save()

        return self.check_in_id

    @staticmethod
    def get(check_in_id: int) -> dict:
        fields = [
            "check_in_id", "check_in_code", "check_in_date", "check_in_status", "remarks_notes",
            "property_id", "property_assignment_id", "tenant_id", "assigned_employee_id",
            "assigned_employee__name",
            "tenant_code", "tenant_name", "tenant_type", "tenant_mobile_number", "tenant_email",
            "tenant_civil_id", "tenant_passport_number", "tenant_nationality", "tenant_address",
            "date_of_birth", "gender", "marital_status", "alternate_mobile_number",
            "emergency_contact_name", "emergency_contact_number", "profession",
            "company_name", "move_in_reason", "number_of_occupants",
            "property_type", "property_code", "building_name", "flat_unit_number",
            "floor_number", "property_status",
            "monthly_rent", "security_deposit", "advance_rent_received", "first_month_rent_paid",
            "payment_mode", "maintenance_charges",
            "inspection_required", "inspection_date", "technician_type", "manager_approval",
            "issue_identified", "supervisor_remarks", "inspection_priority",
            "inspection_type", "inspection_duration", "next_inspection_due",
            "repair_required", "quotation_amount", "inventory_available", "gm_approval",
            "landlord_consent", "finance_alert_generated", "rent_adjustment_amount", "repair_priority",
            "recommended_by_id", "recommended_by__name", "approved_by_id", "approved_by__name",
            "approved_on", "inspector_comments",
            "electricity_meter_reading", "water_meter_reading", "gas_meter_reading",
            "utility_adjustment_amount",
            "agreement_type", "agreement_status", "agreement_start_date", "agreement_end_date",
            "agreement_document",
            "agreement_template", "agreement_number", "generated_on", "generated_by_id",
            "generated_by__name", "submitted_to_tenant_on", "tenant_signed_on",
            "manager_signed_on", "signed_by_id", "signed_by__name",
            "renewal_reminder_date", "auto_reminder_enabled", "agreement_notes",
            "key_number", "key_type", "key_available", "key_booking_date", "confirmation_received",
            "key_delivery_date", "key_handover_status",
            "expected_handover_date", "handover_notes", "tenant_confirmation_notes",
            "key_booked_on", "key_booked_by_id", "key_booked_by__name",
            "key_prepared_on", "key_notified_on", "handover_completed_on",
            "handed_over_by_id", "handed_over_by__name",
            "internal_comments", "tenant_remarks", "special_instructions",
            "property_created_date", "listed_for_rent_date", "tenant_assigned_date",
            "assigned_to_employee_date", "property_occupied_date",
            "created_by_id", "created_by__name", "updated_by_id", "created_at", "updated_at", "status_history",
            "is_active",
        ]
        return CheckIn.objects.filter(check_in_id=check_in_id, is_active=True).values(*fields).first()

    # Fields that should be matched exactly when used as a get_all filter_key
    # (IDs, statuses, and choice fields) — everything else falls back to icontains.
    EXACT_MATCH_FILTER_FIELDS = {
        "check_in_id", "property_id", "tenant_id", "assigned_employee_id",
        "check_in_status", "manager_approval", "key_handover_status", "property_type",
    }

    @staticmethod
    def get_all(
        sort_by: str = None,
        sort_order: str = "asc",
        filter_key: str = None,
        filter_value: str = None,
        search_key: str = None,
        from_date=None,
        to_date=None,
    ) -> list:
        from django.db.models import Q

        query = CheckIn.objects.filter(is_active=True)

        if filter_key and filter_value:
            if filter_key in CheckIn.EXACT_MATCH_FILTER_FIELDS:
                query = query.filter(**{filter_key: filter_value})
            else:
                query = query.filter(**{f"{filter_key}__icontains": filter_value})

        if search_key:
            query = query.filter(
                Q(check_in_code__icontains=search_key) |
                Q(tenant_name__icontains=search_key) |
                Q(building_name__icontains=search_key)
            )

        if from_date:
            query = query.filter(check_in_date__gte=from_date)
        if to_date:
            query = query.filter(check_in_date__lte=to_date)

        if sort_by:
            query = query.order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")
        else:
            query = query.order_by("-created_at")

        fields = [
            "check_in_id", "tenant_id", "tenant_name", "building_name", "flat_unit_number",
            "check_in_date", "monthly_rent", "manager_approval", "key_handover_status",
            "check_in_status", "assigned_employee_id", "assigned_employee__name",
        ]
        return list(query.values(*fields))

    @staticmethod
    def delete(check_in_id: int):
        return CheckIn.objects.filter(check_in_id=check_in_id).update(is_active=False)

    @staticmethod
    def update_information(
        check_in_id: int,
        assigned_employee_id: int = None,
        check_in_date=None,
        check_in_status: str = None,
        remarks_notes: str = None,
        updated_by: int = None,
    ) -> int:
        try:
            check_in = CheckIn.objects.get(check_in_id=check_in_id)
        except CheckIn.DoesNotExist:
            raise ValueError(f"Invalid Check-In Id: {check_in_id}")

        if assigned_employee_id is not None:
            check_in.assigned_employee_id = assigned_employee_id
        if check_in_date is not None:
            check_in.check_in_date = check_in_date
        if check_in_status is not None and check_in_status != check_in.check_in_status:
            check_in.status_history = (
                f"{check_in.status_history}\n{check_in.check_in_status} -> {check_in_status}"
                if check_in.status_history else f"{check_in.check_in_status} -> {check_in_status}"
            )
            check_in.check_in_status = check_in_status
        if remarks_notes is not None:
            check_in.remarks_notes = remarks_notes
        if updated_by is not None:
            check_in.updated_by_id = updated_by

        check_in.save()
        return check_in.check_in_id

    @staticmethod
    def update_tenant_details(
        check_in_id: int,
        tenant_code: str = None,
        tenant_name: str = None,
        tenant_type: str = None,
        tenant_mobile_number: str = None,
        tenant_email: str = None,
        tenant_civil_id: str = None,
        tenant_passport_number: str = None,
        tenant_nationality: str = None,
        tenant_address: str = None,
        date_of_birth=None,
        gender: str = None,
        marital_status: str = None,
        alternate_mobile_number: str = None,
        emergency_contact_name: str = None,
        emergency_contact_number: str = None,
        profession: str = None,
        company_name: str = None,
        move_in_reason: str = None,
        number_of_occupants: int = None,
        updated_by: int = None,
    ) -> int:
        try:
            check_in = CheckIn.objects.get(check_in_id=check_in_id)
        except CheckIn.DoesNotExist:
            raise ValueError(f"Invalid Check-In Id: {check_in_id}")

        if tenant_code is not None:
            check_in.tenant_code = tenant_code
        if tenant_name is not None:
            check_in.tenant_name = tenant_name
        if tenant_type is not None:
            check_in.tenant_type = tenant_type
        if tenant_mobile_number is not None:
            check_in.tenant_mobile_number = tenant_mobile_number
        if tenant_email is not None:
            check_in.tenant_email = tenant_email
        if tenant_civil_id is not None:
            check_in.tenant_civil_id = tenant_civil_id
        if tenant_passport_number is not None:
            check_in.tenant_passport_number = tenant_passport_number
        if tenant_nationality is not None:
            check_in.tenant_nationality = tenant_nationality
        if tenant_address is not None:
            check_in.tenant_address = tenant_address
        if date_of_birth is not None:
            check_in.date_of_birth = date_of_birth
        if gender is not None:
            check_in.gender = gender
        if marital_status is not None:
            check_in.marital_status = marital_status
        if alternate_mobile_number is not None:
            check_in.alternate_mobile_number = alternate_mobile_number
        if emergency_contact_name is not None:
            check_in.emergency_contact_name = emergency_contact_name
        if emergency_contact_number is not None:
            check_in.emergency_contact_number = emergency_contact_number
        if profession is not None:
            check_in.profession = profession
        if company_name is not None:
            check_in.company_name = company_name
        if move_in_reason is not None:
            check_in.move_in_reason = move_in_reason
        if number_of_occupants is not None:
            check_in.number_of_occupants = number_of_occupants
        if updated_by is not None:
            check_in.updated_by_id = updated_by

        check_in.save()
        return check_in.check_in_id

    @staticmethod
    def update_property_details(
        check_in_id: int,
        property_type: str = None,
        property_code: str = None,
        building_name: str = None,
        flat_unit_number: str = None,
        floor_number: str = None,
        property_status: str = None,
        updated_by: int = None,
    ) -> int:
        try:
            check_in = CheckIn.objects.get(check_in_id=check_in_id)
        except CheckIn.DoesNotExist:
            raise ValueError(f"Invalid Check-In Id: {check_in_id}")

        if property_type is not None:
            check_in.property_type = property_type
        if property_code is not None:
            check_in.property_code = property_code
        if building_name is not None:
            check_in.building_name = building_name
        if flat_unit_number is not None:
            check_in.flat_unit_number = flat_unit_number
        if floor_number is not None:
            check_in.floor_number = floor_number
        if property_status is not None:
            check_in.property_status = property_status
        if updated_by is not None:
            check_in.updated_by_id = updated_by

        check_in.save()
        return check_in.check_in_id

    @staticmethod
    def update_rental_details(
        check_in_id: int,
        monthly_rent=None,
        security_deposit=None,
        advance_rent_received=None,
        first_month_rent_paid=None,
        payment_mode: str = None,
        maintenance_charges=None,
        updated_by: int = None,
    ) -> int:
        try:
            check_in = CheckIn.objects.get(check_in_id=check_in_id)
        except CheckIn.DoesNotExist:
            raise ValueError(f"Invalid Check-In Id: {check_in_id}")

        if monthly_rent is not None:
            check_in.monthly_rent = monthly_rent
        if security_deposit is not None:
            check_in.security_deposit = security_deposit
        if advance_rent_received is not None:
            check_in.advance_rent_received = advance_rent_received
        if first_month_rent_paid is not None:
            check_in.first_month_rent_paid = first_month_rent_paid
        if payment_mode is not None:
            check_in.payment_mode = payment_mode
        if maintenance_charges is not None:
            check_in.maintenance_charges = maintenance_charges
        if updated_by is not None:
            check_in.updated_by_id = updated_by

        check_in.save()
        return check_in.check_in_id

    @staticmethod
    def update_property_inspection(
        check_in_id: int,
        inspection_required: str = None,
        inspection_date=None,
        technician_type: str = None,
        manager_approval: str = None,
        issue_identified: str = None,
        supervisor_remarks: str = None,
        inspection_priority: str = None,
        inspection_type: str = None,
        inspection_duration: str = None,
        next_inspection_due=None,
        updated_by: int = None,
    ) -> int:
        try:
            check_in = CheckIn.objects.get(check_in_id=check_in_id)
        except CheckIn.DoesNotExist:
            raise ValueError(f"Invalid Check-In Id: {check_in_id}")

        if inspection_required is not None:
            check_in.inspection_required = inspection_required
        if inspection_date is not None:
            check_in.inspection_date = inspection_date
        if technician_type is not None:
            check_in.technician_type = technician_type
        if manager_approval is not None:
            check_in.manager_approval = manager_approval
        if issue_identified is not None:
            check_in.issue_identified = issue_identified
        if supervisor_remarks is not None:
            check_in.supervisor_remarks = supervisor_remarks
        if inspection_priority is not None:
            check_in.inspection_priority = inspection_priority
        if inspection_type is not None:
            check_in.inspection_type = inspection_type
        if inspection_duration is not None:
            check_in.inspection_duration = inspection_duration
        if next_inspection_due is not None:
            check_in.next_inspection_due = next_inspection_due
        if updated_by is not None:
            check_in.updated_by_id = updated_by

        check_in.save()
        return check_in.check_in_id

    @staticmethod
    def update_repair_approval(
        check_in_id: int,
        repair_required: str = None,
        quotation_amount=None,
        inventory_available: str = None,
        gm_approval: str = None,
        landlord_consent: str = None,
        finance_alert_generated: str = None,
        rent_adjustment_amount=None,
        repair_priority: str = None,
        recommended_by_id: int = None,
        approved_by_id: int = None,
        approved_on=None,
        inspector_comments: str = None,
        updated_by: int = None,
    ) -> int:
        try:
            check_in = CheckIn.objects.get(check_in_id=check_in_id)
        except CheckIn.DoesNotExist:
            raise ValueError(f"Invalid Check-In Id: {check_in_id}")

        if repair_required is not None:
            check_in.repair_required = repair_required
        if quotation_amount is not None:
            check_in.quotation_amount = quotation_amount
        if inventory_available is not None:
            check_in.inventory_available = inventory_available
        if gm_approval is not None:
            check_in.gm_approval = gm_approval
        if landlord_consent is not None:
            check_in.landlord_consent = landlord_consent
        if finance_alert_generated is not None:
            check_in.finance_alert_generated = finance_alert_generated
        if rent_adjustment_amount is not None:
            check_in.rent_adjustment_amount = rent_adjustment_amount
        if repair_priority is not None:
            check_in.repair_priority = repair_priority
        if recommended_by_id is not None:
            check_in.recommended_by_id = recommended_by_id
        if approved_by_id is not None:
            check_in.approved_by_id = approved_by_id
        if approved_on is not None:
            check_in.approved_on = approved_on
        if inspector_comments is not None:
            check_in.inspector_comments = inspector_comments
        if updated_by is not None:
            check_in.updated_by_id = updated_by

        check_in.save()
        return check_in.check_in_id

    @staticmethod
    def update_utility_meter_readings(
        check_in_id: int,
        electricity_meter_reading=None,
        water_meter_reading=None,
        gas_meter_reading=None,
        utility_adjustment_amount=None,
        updated_by: int = None,
    ) -> int:
        try:
            check_in = CheckIn.objects.get(check_in_id=check_in_id)
        except CheckIn.DoesNotExist:
            raise ValueError(f"Invalid Check-In Id: {check_in_id}")

        if electricity_meter_reading is not None:
            check_in.electricity_meter_reading = electricity_meter_reading
        if water_meter_reading is not None:
            check_in.water_meter_reading = water_meter_reading
        if gas_meter_reading is not None:
            check_in.gas_meter_reading = gas_meter_reading
        if utility_adjustment_amount is not None:
            check_in.utility_adjustment_amount = utility_adjustment_amount
        if updated_by is not None:
            check_in.updated_by_id = updated_by

        check_in.save()
        return check_in.check_in_id

    @staticmethod
    def update_agreement_details(
        check_in_id: int,
        agreement_type: str = None,
        agreement_status: str = None,
        agreement_start_date=None,
        agreement_end_date=None,
        agreement_document_processed=None,
        agreement_template: str = None,
        agreement_number: str = None,
        generated_on=None,
        generated_by_id: int = None,
        submitted_to_tenant_on=None,
        tenant_signed_on=None,
        manager_signed_on=None,
        signed_by_id: int = None,
        renewal_reminder_date=None,
        auto_reminder_enabled: bool = None,
        agreement_notes: str = None,
        updated_by: int = None,
    ) -> int:
        try:
            check_in = CheckIn.objects.get(check_in_id=check_in_id)
        except CheckIn.DoesNotExist:
            raise ValueError(f"Invalid Check-In Id: {check_in_id}")

        if agreement_type is not None:
            check_in.agreement_type = agreement_type
        if agreement_status is not None:
            check_in.agreement_status = agreement_status
        if agreement_start_date is not None:
            check_in.agreement_start_date = agreement_start_date
        if agreement_end_date is not None:
            check_in.agreement_end_date = agreement_end_date
        if agreement_document_processed is not None:
            if isinstance(agreement_document_processed, tuple) and agreement_document_processed[0] == 'url':
                check_in.agreement_document = agreement_document_processed[1]
            else:
                check_in.agreement_document.save(
                    agreement_document_processed.name, agreement_document_processed, save=False
                )
        if agreement_template is not None:
            check_in.agreement_template = agreement_template
        if agreement_number is not None:
            check_in.agreement_number = agreement_number
        if generated_on is not None:
            check_in.generated_on = generated_on
        if generated_by_id is not None:
            check_in.generated_by_id = generated_by_id
        if submitted_to_tenant_on is not None:
            check_in.submitted_to_tenant_on = submitted_to_tenant_on
        if tenant_signed_on is not None:
            check_in.tenant_signed_on = tenant_signed_on
        if manager_signed_on is not None:
            check_in.manager_signed_on = manager_signed_on
        if signed_by_id is not None:
            check_in.signed_by_id = signed_by_id
        if renewal_reminder_date is not None:
            check_in.renewal_reminder_date = renewal_reminder_date
        if auto_reminder_enabled is not None:
            check_in.auto_reminder_enabled = auto_reminder_enabled
        if agreement_notes is not None:
            check_in.agreement_notes = agreement_notes
        if updated_by is not None:
            check_in.updated_by_id = updated_by

        check_in.save()
        return check_in.check_in_id

    @staticmethod
    def update_key_handover(
        check_in_id: int,
        key_number: str = None,
        key_type: str = None,
        key_available: str = None,
        key_booking_date=None,
        confirmation_received: str = None,
        key_delivery_date=None,
        key_handover_status: str = None,
        expected_handover_date=None,
        handover_notes: str = None,
        tenant_confirmation_notes: str = None,
        key_booked_on=None,
        key_booked_by_id: int = None,
        key_prepared_on=None,
        key_notified_on=None,
        handover_completed_on=None,
        handed_over_by_id: int = None,
        updated_by: int = None,
    ) -> int:
        try:
            check_in = CheckIn.objects.get(check_in_id=check_in_id)
        except CheckIn.DoesNotExist:
            raise ValueError(f"Invalid Check-In Id: {check_in_id}")

        if key_number is not None:
            check_in.key_number = key_number
        if key_type is not None:
            check_in.key_type = key_type
        if key_available is not None:
            check_in.key_available = key_available
        if key_booking_date is not None:
            check_in.key_booking_date = key_booking_date
        if confirmation_received is not None:
            check_in.confirmation_received = confirmation_received
        if key_delivery_date is not None:
            check_in.key_delivery_date = key_delivery_date
        if key_handover_status is not None:
            check_in.key_handover_status = key_handover_status
        if expected_handover_date is not None:
            check_in.expected_handover_date = expected_handover_date
        if handover_notes is not None:
            check_in.handover_notes = handover_notes
        if tenant_confirmation_notes is not None:
            check_in.tenant_confirmation_notes = tenant_confirmation_notes
        if key_booked_on is not None:
            check_in.key_booked_on = key_booked_on
        if key_booked_by_id is not None:
            check_in.key_booked_by_id = key_booked_by_id
        if key_prepared_on is not None:
            check_in.key_prepared_on = key_prepared_on
        if key_notified_on is not None:
            check_in.key_notified_on = key_notified_on
        if handover_completed_on is not None:
            check_in.handover_completed_on = handover_completed_on
        if handed_over_by_id is not None:
            check_in.handed_over_by_id = handed_over_by_id
        if updated_by is not None:
            check_in.updated_by_id = updated_by

        check_in.save()
        return check_in.check_in_id

    @staticmethod
    def update_comments(
        check_in_id: int,
        internal_comments: str = None,
        tenant_remarks: str = None,
        special_instructions: str = None,
        updated_by: int = None,
    ) -> int:
        try:
            check_in = CheckIn.objects.get(check_in_id=check_in_id)
        except CheckIn.DoesNotExist:
            raise ValueError(f"Invalid Check-In Id: {check_in_id}")

        if internal_comments is not None:
            check_in.internal_comments = internal_comments
        if tenant_remarks is not None:
            check_in.tenant_remarks = tenant_remarks
        if special_instructions is not None:
            check_in.special_instructions = special_instructions
        if updated_by is not None:
            check_in.updated_by_id = updated_by

        check_in.save()
        return check_in.check_in_id
