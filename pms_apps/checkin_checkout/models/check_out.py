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

    def create(
        self,
        property_id: int,
        created_by: int,
        property_assignment_id: int = None,
        check_in_id: int = None,
        tenant_id: int = None,
        assigned_employee_id: int = None,
        check_out_date=None,
        check_out_status: str = "Pending",
        remarks_notes: str = "",
        tenant_code: str = None,
        tenant_name: str = None,
        tenant_type: str = None,
        tenant_mobile_number: str = None,
        tenant_email: str = None,
        tenant_civil_id: str = None,
        tenant_passport_number: str = None,
        tenant_nationality: str = None,
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
        repair_required: str = None,
        quotation_amount=None,
        inventory_available: str = None,
        gm_approval: str = None,
        landlord_consent: str = None,
        finance_alert_generated: str = None,
        rent_adjustment_amount=None,
        electricity_meter_reading=None,
        water_meter_reading=None,
        gas_meter_reading=None,
        charge_type: str = None,
        total_amount=None,
        payment_status: str = None,
        payment_date=None,
        transaction_id: str = None,
        key_number: str = None,
        key_return: str = None,
        expected_return_date=None,
        confirmation_received: str = None,
        key_return_date=None,
        key_return_status: str = "Pending",
        internal_comments: str = "",
        tenant_remarks: str = "",
        special_instructions: str = "",
    ) -> int:
        self.property_id = property_id
        self.property_assignment_id = property_assignment_id
        self.check_in_id = check_in_id
        self.tenant_id = tenant_id
        self.assigned_employee_id = assigned_employee_id
        self.created_by_id = created_by

        # A. Check-Out Information
        self.check_out_date = check_out_date
        self.check_out_status = check_out_status
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

        # F. Repair & Damage
        self.repair_required = repair_required
        self.quotation_amount = quotation_amount
        self.inventory_available = inventory_available
        self.gm_approval = gm_approval
        self.landlord_consent = landlord_consent
        self.finance_alert_generated = finance_alert_generated
        self.rent_adjustment_amount = rent_adjustment_amount

        # G. Check-Out Utility Meter Readings
        self.electricity_meter_reading = electricity_meter_reading
        self.water_meter_reading = water_meter_reading
        self.gas_meter_reading = gas_meter_reading

        # H. Finance Details
        self.charge_type = charge_type
        self.total_amount = total_amount
        self.payment_status = payment_status
        self.payment_date = payment_date
        self.transaction_id = transaction_id

        # I. Key Return
        self.key_number = key_number
        self.key_return = key_return
        self.expected_return_date = expected_return_date
        self.confirmation_received = confirmation_received
        self.key_return_date = key_return_date
        self.key_return_status = key_return_status

        # K. Comments
        self.internal_comments = internal_comments
        self.tenant_remarks = tenant_remarks
        self.special_instructions = special_instructions

        self.save()

        # Auto-generate the business code now that the primary key exists
        self.check_out_code = f"CHKOUT-{self.check_out_id:06d}"
        self.status_history = f"Created -> {self.check_out_status}"
        self.save()

        return self.check_out_id

    @staticmethod
    def get(check_out_id: int) -> dict:
        fields = [
            "check_out_id", "check_out_code", "check_out_date", "check_out_status", "remarks_notes",
            "property_id", "property_assignment_id", "check_in_id", "tenant_id", "assigned_employee_id",
            "assigned_employee__name",
            "tenant_code", "tenant_name", "tenant_type", "tenant_mobile_number", "tenant_email",
            "tenant_civil_id", "tenant_passport_number", "tenant_nationality",
            "property_type", "property_code", "building_name", "flat_unit_number",
            "floor_number", "property_status",
            "monthly_rent", "security_deposit", "advance_rent_received", "first_month_rent_paid",
            "payment_mode", "maintenance_charges",
            "inspection_required", "inspection_date", "technician_type", "manager_approval",
            "issue_identified", "supervisor_remarks",
            "repair_required", "quotation_amount", "inventory_available", "gm_approval",
            "landlord_consent", "finance_alert_generated", "rent_adjustment_amount",
            "electricity_meter_reading", "water_meter_reading", "gas_meter_reading",
            "charge_type", "total_amount", "payment_status", "payment_date", "transaction_id",
            "payment_proof",
            "key_number", "key_return", "expected_return_date", "confirmation_received",
            "key_return_date", "key_return_status",
            "internal_comments", "tenant_remarks", "special_instructions",
            "created_by_id", "created_by__name", "updated_by_id", "created_at", "updated_at",
            "status_history", "is_active",
        ]
        return CheckOut.objects.filter(check_out_id=check_out_id, is_active=True).values(*fields).first()

    # Fields that should be matched exactly when used as a get_all filter_key
    # (IDs, statuses, and choice fields) — everything else falls back to icontains.
    EXACT_MATCH_FILTER_FIELDS = {
        "check_out_id", "property_id", "tenant_id", "assigned_employee_id",
        "check_out_status", "manager_approval", "key_return_status", "property_type",
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

        query = CheckOut.objects.filter(is_active=True)

        if filter_key and filter_value:
            if filter_key in CheckOut.EXACT_MATCH_FILTER_FIELDS:
                query = query.filter(**{filter_key: filter_value})
            else:
                query = query.filter(**{f"{filter_key}__icontains": filter_value})

        if search_key:
            query = query.filter(
                Q(check_out_code__icontains=search_key) |
                Q(tenant_name__icontains=search_key) |
                Q(building_name__icontains=search_key)
            )

        if from_date:
            query = query.filter(check_out_date__gte=from_date)
        if to_date:
            query = query.filter(check_out_date__lte=to_date)

        if sort_by:
            query = query.order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")
        else:
            query = query.order_by("-created_at")

        fields = [
            "check_out_id", "tenant_id", "tenant_name", "building_name", "flat_unit_number",
            "check_out_date", "monthly_rent", "manager_approval", "key_return_status",
            "check_out_status", "assigned_employee_id", "assigned_employee__name",
        ]
        return list(query.values(*fields))

    @staticmethod
    def delete(check_out_id: int):
        return CheckOut.objects.filter(check_out_id=check_out_id).update(is_active=False)

    @staticmethod
    def update_information(
        check_out_id: int,
        assigned_employee_id: int = None,
        check_out_date=None,
        check_out_status: str = None,
        remarks_notes: str = None,
        updated_by: int = None,
    ) -> int:
        try:
            check_out = CheckOut.objects.get(check_out_id=check_out_id)
        except CheckOut.DoesNotExist:
            raise ValueError(f"Invalid Check-Out Id: {check_out_id}")

        if assigned_employee_id is not None:
            check_out.assigned_employee_id = assigned_employee_id
        if check_out_date is not None:
            check_out.check_out_date = check_out_date
        if check_out_status is not None and check_out_status != check_out.check_out_status:
            check_out.status_history = (
                f"{check_out.status_history}\n{check_out.check_out_status} -> {check_out_status}"
                if check_out.status_history else f"{check_out.check_out_status} -> {check_out_status}"
            )
            check_out.check_out_status = check_out_status
        if remarks_notes is not None:
            check_out.remarks_notes = remarks_notes
        if updated_by is not None:
            check_out.updated_by_id = updated_by

        check_out.save()
        return check_out.check_out_id

    @staticmethod
    def update_tenant_details(
        check_out_id: int,
        tenant_code: str = None,
        tenant_name: str = None,
        tenant_type: str = None,
        tenant_mobile_number: str = None,
        tenant_email: str = None,
        tenant_civil_id: str = None,
        tenant_passport_number: str = None,
        tenant_nationality: str = None,
        updated_by: int = None,
    ) -> int:
        try:
            check_out = CheckOut.objects.get(check_out_id=check_out_id)
        except CheckOut.DoesNotExist:
            raise ValueError(f"Invalid Check-Out Id: {check_out_id}")

        if tenant_code is not None:
            check_out.tenant_code = tenant_code
        if tenant_name is not None:
            check_out.tenant_name = tenant_name
        if tenant_type is not None:
            check_out.tenant_type = tenant_type
        if tenant_mobile_number is not None:
            check_out.tenant_mobile_number = tenant_mobile_number
        if tenant_email is not None:
            check_out.tenant_email = tenant_email
        if tenant_civil_id is not None:
            check_out.tenant_civil_id = tenant_civil_id
        if tenant_passport_number is not None:
            check_out.tenant_passport_number = tenant_passport_number
        if tenant_nationality is not None:
            check_out.tenant_nationality = tenant_nationality
        if updated_by is not None:
            check_out.updated_by_id = updated_by

        check_out.save()
        return check_out.check_out_id

    @staticmethod
    def update_property_details(
        check_out_id: int,
        property_type: str = None,
        property_code: str = None,
        building_name: str = None,
        flat_unit_number: str = None,
        floor_number: str = None,
        property_status: str = None,
        updated_by: int = None,
    ) -> int:
        try:
            check_out = CheckOut.objects.get(check_out_id=check_out_id)
        except CheckOut.DoesNotExist:
            raise ValueError(f"Invalid Check-Out Id: {check_out_id}")

        if property_type is not None:
            check_out.property_type = property_type
        if property_code is not None:
            check_out.property_code = property_code
        if building_name is not None:
            check_out.building_name = building_name
        if flat_unit_number is not None:
            check_out.flat_unit_number = flat_unit_number
        if floor_number is not None:
            check_out.floor_number = floor_number
        if property_status is not None:
            check_out.property_status = property_status
        if updated_by is not None:
            check_out.updated_by_id = updated_by

        check_out.save()
        return check_out.check_out_id

    @staticmethod
    def update_rental_details(
        check_out_id: int,
        monthly_rent=None,
        security_deposit=None,
        advance_rent_received=None,
        first_month_rent_paid=None,
        payment_mode: str = None,
        maintenance_charges=None,
        updated_by: int = None,
    ) -> int:
        try:
            check_out = CheckOut.objects.get(check_out_id=check_out_id)
        except CheckOut.DoesNotExist:
            raise ValueError(f"Invalid Check-Out Id: {check_out_id}")

        if monthly_rent is not None:
            check_out.monthly_rent = monthly_rent
        if security_deposit is not None:
            check_out.security_deposit = security_deposit
        if advance_rent_received is not None:
            check_out.advance_rent_received = advance_rent_received
        if first_month_rent_paid is not None:
            check_out.first_month_rent_paid = first_month_rent_paid
        if payment_mode is not None:
            check_out.payment_mode = payment_mode
        if maintenance_charges is not None:
            check_out.maintenance_charges = maintenance_charges
        if updated_by is not None:
            check_out.updated_by_id = updated_by

        check_out.save()
        return check_out.check_out_id

    @staticmethod
    def update_property_inspection(
        check_out_id: int,
        inspection_required: str = None,
        inspection_date=None,
        technician_type: str = None,
        manager_approval: str = None,
        issue_identified: str = None,
        supervisor_remarks: str = None,
        updated_by: int = None,
    ) -> int:
        try:
            check_out = CheckOut.objects.get(check_out_id=check_out_id)
        except CheckOut.DoesNotExist:
            raise ValueError(f"Invalid Check-Out Id: {check_out_id}")

        if inspection_required is not None:
            check_out.inspection_required = inspection_required
        if inspection_date is not None:
            check_out.inspection_date = inspection_date
        if technician_type is not None:
            check_out.technician_type = technician_type
        if manager_approval is not None:
            check_out.manager_approval = manager_approval
        if issue_identified is not None:
            check_out.issue_identified = issue_identified
        if supervisor_remarks is not None:
            check_out.supervisor_remarks = supervisor_remarks
        if updated_by is not None:
            check_out.updated_by_id = updated_by

        check_out.save()
        return check_out.check_out_id

    @staticmethod
    def update_repair_damage(
        check_out_id: int,
        repair_required: str = None,
        quotation_amount=None,
        inventory_available: str = None,
        gm_approval: str = None,
        landlord_consent: str = None,
        finance_alert_generated: str = None,
        rent_adjustment_amount=None,
        updated_by: int = None,
    ) -> int:
        try:
            check_out = CheckOut.objects.get(check_out_id=check_out_id)
        except CheckOut.DoesNotExist:
            raise ValueError(f"Invalid Check-Out Id: {check_out_id}")

        if repair_required is not None:
            check_out.repair_required = repair_required
        if quotation_amount is not None:
            check_out.quotation_amount = quotation_amount
        if inventory_available is not None:
            check_out.inventory_available = inventory_available
        if gm_approval is not None:
            check_out.gm_approval = gm_approval
        if landlord_consent is not None:
            check_out.landlord_consent = landlord_consent
        if finance_alert_generated is not None:
            check_out.finance_alert_generated = finance_alert_generated
        if rent_adjustment_amount is not None:
            check_out.rent_adjustment_amount = rent_adjustment_amount
        if updated_by is not None:
            check_out.updated_by_id = updated_by

        check_out.save()
        return check_out.check_out_id

    @staticmethod
    def update_utility_meter_readings(
        check_out_id: int,
        electricity_meter_reading=None,
        water_meter_reading=None,
        gas_meter_reading=None,
        updated_by: int = None,
    ) -> int:
        try:
            check_out = CheckOut.objects.get(check_out_id=check_out_id)
        except CheckOut.DoesNotExist:
            raise ValueError(f"Invalid Check-Out Id: {check_out_id}")

        if electricity_meter_reading is not None:
            check_out.electricity_meter_reading = electricity_meter_reading
        if water_meter_reading is not None:
            check_out.water_meter_reading = water_meter_reading
        if gas_meter_reading is not None:
            check_out.gas_meter_reading = gas_meter_reading
        if updated_by is not None:
            check_out.updated_by_id = updated_by

        check_out.save()
        return check_out.check_out_id

    @staticmethod
    def update_finance_details(
        check_out_id: int,
        charge_type: str = None,
        total_amount=None,
        payment_status: str = None,
        payment_date=None,
        transaction_id: str = None,
        payment_proof_processed=None,
        updated_by: int = None,
    ) -> int:
        try:
            check_out = CheckOut.objects.get(check_out_id=check_out_id)
        except CheckOut.DoesNotExist:
            raise ValueError(f"Invalid Check-Out Id: {check_out_id}")

        if charge_type is not None:
            check_out.charge_type = charge_type
        if total_amount is not None:
            check_out.total_amount = total_amount
        if payment_status is not None:
            check_out.payment_status = payment_status
        if payment_date is not None:
            check_out.payment_date = payment_date
        if transaction_id is not None:
            check_out.transaction_id = transaction_id
        if payment_proof_processed is not None:
            if isinstance(payment_proof_processed, tuple) and payment_proof_processed[0] == 'url':
                check_out.payment_proof = payment_proof_processed[1]
            else:
                check_out.payment_proof.save(
                    payment_proof_processed.name, payment_proof_processed, save=False
                )
        if updated_by is not None:
            check_out.updated_by_id = updated_by

        check_out.save()
        return check_out.check_out_id

    @staticmethod
    def update_key_return(
        check_out_id: int,
        key_number: str = None,
        key_return: str = None,
        expected_return_date=None,
        confirmation_received: str = None,
        key_return_date=None,
        key_return_status: str = None,
        updated_by: int = None,
    ) -> int:
        try:
            check_out = CheckOut.objects.get(check_out_id=check_out_id)
        except CheckOut.DoesNotExist:
            raise ValueError(f"Invalid Check-Out Id: {check_out_id}")

        if key_number is not None:
            check_out.key_number = key_number
        if key_return is not None:
            check_out.key_return = key_return
        if expected_return_date is not None:
            check_out.expected_return_date = expected_return_date
        if confirmation_received is not None:
            check_out.confirmation_received = confirmation_received
        if key_return_date is not None:
            check_out.key_return_date = key_return_date
        if key_return_status is not None:
            check_out.key_return_status = key_return_status
        if updated_by is not None:
            check_out.updated_by_id = updated_by

        check_out.save()
        return check_out.check_out_id

    @staticmethod
    def update_comments(
        check_out_id: int,
        internal_comments: str = None,
        tenant_remarks: str = None,
        special_instructions: str = None,
        updated_by: int = None,
    ) -> int:
        try:
            check_out = CheckOut.objects.get(check_out_id=check_out_id)
        except CheckOut.DoesNotExist:
            raise ValueError(f"Invalid Check-Out Id: {check_out_id}")

        if internal_comments is not None:
            check_out.internal_comments = internal_comments
        if tenant_remarks is not None:
            check_out.tenant_remarks = tenant_remarks
        if special_instructions is not None:
            check_out.special_instructions = special_instructions
        if updated_by is not None:
            check_out.updated_by_id = updated_by

        check_out.save()
        return check_out.check_out_id
