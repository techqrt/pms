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
        ("Rent", "Rent"),
        ("Maintenance", "Maintenance"),
        ("Damage", "Damage"),
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

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical"),
    ]

    SETTLEMENT_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Settled", "Settled"),
        ("Partially Settled", "Partially Settled"),
    ]

    REQUEST_FROM_CHOICES = [
        ("Tenant", "Tenant"),
        ("Admin", "Admin"),
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
    request_from = models.CharField(
        max_length=10, choices=REQUEST_FROM_CHOICES, null=True, blank=True
    )

    # B. Tenant Details — sourced live from Lead via tenant FK
    # C. Property Details — sourced live from Property/PropertyDetail via property FK

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
    inspection_duration = models.CharField(max_length=20, null=True, blank=True)
    manager_approval = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        null=True,
        blank=True
    )
    issue_identified = models.TextField(blank=True, default="")
    supervisor_remarks = models.TextField(blank=True, default="")
    inspection_priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, null=True, blank=True)
    next_inspection_due = models.DateField(null=True, blank=True)

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
    repair_priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, null=True, blank=True)
    recommended_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_outs_recommended"
    )
    approved_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="check_outs_approved"
    )
    approved_on = models.DateField(null=True, blank=True)

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
    settlement_status = models.CharField(max_length=30, choices=SETTLEMENT_STATUS_CHOICES, null=True, blank=True)
    finance_description = models.TextField(blank=True, default="")
    payment_proof = models.FileField(
        upload_to="checkin_checkout/payment_proofs/",
        max_length=500,
        null=True,
        blank=True
    )

    # I. Key Return
    key_number = models.CharField(max_length=100, null=True, blank=True)
    key_type = models.CharField(max_length=100, null=True, blank=True)
    key_available = models.CharField(max_length=10, choices=YES_NO_CHOICES, null=True, blank=True)
    key_return = models.CharField(
        max_length=10,
        choices=YES_NO_CHOICES,
        null=True,
        blank=True
    )
    expected_return_date = models.DateField(null=True, blank=True)
    key_booking_date = models.DateField(null=True, blank=True)
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
        request_from: str = None,
        monthly_rent=None,
        security_deposit=None,
        advance_rent_received=None,
        first_month_rent_paid=None,
        payment_mode: str = None,
        maintenance_charges=None,
        inspection_required: str = None,
        inspection_date=None,
        technician_type: str = None,
        inspection_duration: str = None,
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
        self.request_from = request_from

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
        self.inspection_duration = inspection_duration
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
    def _tenant_data(tenant_id: int) -> dict:
        from pms_apps.lead.models.lead import Lead as LeadModel
        if not tenant_id:
            return {}
        row = LeadModel.objects.filter(lead_id=tenant_id).values(
            'first_name', 'last_name', 'lead_id__phone_number', 'lead_id__email',
            'civil_id', 'passport_or_id', 'nationality__name', 'address',
            'tenant_code', 'tenant_type', 'date_of_birth', 'gender', 'marital_status',
            'emergency_contact_name', 'emergency_contact_number', 'profession', 'company_name',
        ).first() or {}
        return {
            'tenant_name': f"{row.get('first_name') or ''} {row.get('last_name') or ''}".strip() or None,
            'tenant_mobile_number': row.get('lead_id__phone_number'),
            'tenant_email': row.get('lead_id__email'),
            'tenant_civil_id': row.get('civil_id'),
            'tenant_passport_number': row.get('passport_or_id'),
            'tenant_nationality': row.get('nationality__name'),
            'tenant_address': row.get('address'),
            'tenant_code': row.get('tenant_code'),
            'tenant_type': row.get('tenant_type'),
            'date_of_birth': row.get('date_of_birth'),
            'gender': row.get('gender'),
            'marital_status': row.get('marital_status'),
            'emergency_contact_name': row.get('emergency_contact_name'),
            'emergency_contact_number': row.get('emergency_contact_number'),
            'profession': row.get('profession'),
            'company_name': row.get('company_name'),
        }

    @staticmethod
    def _property_data(property_id: int) -> dict:
        from pms_apps.property.models.property import Property as PropertyModel
        from pms_apps.property.models.property_details import PropertyDetail
        if not property_id:
            return {}
        prop = PropertyModel.objects.filter(property_id=property_id).values('rental_type').first() or {}
        detail = PropertyDetail.objects.filter(property_id=property_id).values(
            'property_code', 'building_name', 'floor_number', 'current_status',
            'flat_number', 'commercial_category', 'villa_name',
        ).first() or {}
        rental_type = prop.get('rental_type')
        if rental_type == 'Flat':
            unit = detail.get('flat_number')
        elif rental_type == 'Commercial':
            unit = detail.get('commercial_category')
        elif rental_type == 'Villa':
            unit = detail.get('villa_name')
        else:
            unit = None
        return {
            'property_type': rental_type,
            'property_code': str(detail['property_code']) if detail.get('property_code') else None,
            'building_name': detail.get('building_name'),
            'flat_unit_number': unit,
            'floor_number': str(detail['floor_number']) if detail.get('floor_number') is not None else None,
            'property_status': detail.get('current_status'),
        }

    @staticmethod
    def get(check_out_id: int) -> dict:
        own_fields = [
            "check_out_id", "check_out_code", "check_out_date", "check_out_status", "remarks_notes",
            "request_from", "property_id", "property_assignment_id", "check_in_id", "tenant_id",
            "assigned_employee_id", "assigned_employee__name",
            "monthly_rent", "security_deposit", "advance_rent_received", "first_month_rent_paid",
            "payment_mode", "maintenance_charges",
            "inspection_required", "inspection_date", "technician_type", "inspection_duration", "manager_approval",
            "inspection_priority", "issue_identified", "supervisor_remarks", "next_inspection_due",
            "repair_required", "quotation_amount", "inventory_available", "gm_approval",
            "landlord_consent", "finance_alert_generated", "rent_adjustment_amount", "repair_priority",
            "recommended_by_id", "recommended_by__name", "approved_by_id", "approved_by__name", "approved_on",
            "electricity_meter_reading", "water_meter_reading", "gas_meter_reading",
            "charge_type", "total_amount", "payment_status", "payment_date", "transaction_id",
            "settlement_status", "finance_description", "payment_proof",
            "key_number", "key_type", "key_available", "key_return", "expected_return_date",
            "key_booking_date", "confirmation_received", "key_return_date", "key_return_status",
            "internal_comments", "tenant_remarks", "special_instructions",
            "created_by_id", "created_by__name", "updated_by_id", "created_at", "updated_at",
            "status_history", "is_active",
        ]
        row = CheckOut.objects.filter(check_out_id=check_out_id, is_active=True).values(*own_fields).first()
        if not row:
            return None
        row.update(CheckOut._tenant_data(row.get('tenant_id')))
        row.update(CheckOut._property_data(row.get('property_id')))
        return row

    EXACT_MATCH_FILTER_FIELDS = {
        "check_out_id", "property_id", "tenant_id", "assigned_employee_id",
        "check_out_status", "manager_approval", "key_return_status",
        "payment_status", "request_from",
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
                Q(tenant__first_name__icontains=search_key) |
                Q(tenant__last_name__icontains=search_key)
            )

        if from_date:
            query = query.filter(check_out_date__gte=from_date)
        if to_date:
            query = query.filter(check_out_date__lte=to_date)

        if sort_by:
            query = query.order_by(f"{'-' if sort_order == 'desc' else ''}{sort_by}")
        else:
            query = query.order_by("-created_at")

        own_fields = [
            "check_out_id", "check_out_code", "tenant_id", "property_id",
            "check_out_date", "security_deposit", "manager_approval", "key_return_status",
            "payment_status", "check_out_status", "request_from",
            "assigned_employee_id", "assigned_employee__name",
        ]
        rows = list(query.values(*own_fields))
        if not rows:
            return []

        from pms_apps.lead.models.lead import Lead as LeadModel
        from pms_apps.property.models.property_details import PropertyDetail
        from pms_apps.property.models.property import Property as PropertyModel

        tenant_ids = {r['tenant_id'] for r in rows if r.get('tenant_id')}
        property_ids = {r['property_id'] for r in rows if r.get('property_id')}

        tenant_map = {}
        for t in LeadModel.objects.filter(lead_id__in=tenant_ids).values('lead_id', 'first_name', 'last_name', 'tenant_code'):
            name = f"{t.get('first_name') or ''} {t.get('last_name') or ''}".strip() or None
            tenant_map[t['lead_id']] = {'name': name, 'tenant_code': t.get('tenant_code')}

        prop_type_map = {p['property_id']: p['rental_type']
                         for p in PropertyModel.objects.filter(property_id__in=property_ids).values('property_id', 'rental_type')}
        detail_map = {d['property_id']: d for d in PropertyDetail.objects.filter(property_id__in=property_ids).values(
            'property_id', 'building_name', 'flat_number', 'commercial_category', 'villa_name'
        )}

        for row in rows:
            tid = row.pop('tenant_id', None)
            pid = row.pop('property_id', None)
            row['tenant_id'] = tid
            tenant_info = tenant_map.get(tid) or {}
            row['tenant_name'] = tenant_info.get('name')
            row['tenant_code'] = tenant_info.get('tenant_code')
            d = detail_map.get(pid) or {}
            row['building_name'] = d.get('building_name')
            rtype = prop_type_map.get(pid)
            if rtype == 'Flat':
                row['flat_unit_number'] = d.get('flat_number')
            elif rtype == 'Commercial':
                row['flat_unit_number'] = d.get('commercial_category')
            elif rtype == 'Villa':
                row['flat_unit_number'] = d.get('villa_name')
            else:
                row['flat_unit_number'] = None

        return rows

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
        request_from: str = None,
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
        if request_from is not None:
            check_out.request_from = request_from
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
        tenant_address: str = None,
        date_of_birth=None,
        gender: str = None,
        marital_status: str = None,
        emergency_contact_name: str = None,
        emergency_contact_number: str = None,
        profession: str = None,
        company_name: str = None,
        updated_by: int = None,
    ) -> int:
        from pms_apps.lead.models.lead import Lead as LeadModel
        from pms_apps.authentication.models import User
        from pms_apps.helper_apis.models.nationality import Nationality

        try:
            check_out = CheckOut.objects.get(check_out_id=check_out_id)
        except CheckOut.DoesNotExist:
            raise ValueError(f"Invalid Check-Out Id: {check_out_id}")

        if check_out.tenant_id:
            lead = LeadModel.objects.filter(lead_id=check_out.tenant_id).first()
            if lead:
                if tenant_name is not None:
                    parts = tenant_name.split(' ', 1)
                    lead.first_name = parts[0]
                    lead.last_name = parts[1] if len(parts) > 1 else lead.last_name
                if tenant_code is not None:
                    lead.tenant_code = tenant_code
                if tenant_type is not None:
                    lead.tenant_type = tenant_type
                if tenant_civil_id is not None:
                    lead.civil_id = tenant_civil_id
                if tenant_passport_number is not None:
                    lead.passport_or_id = tenant_passport_number
                if tenant_nationality is not None:
                    nat = Nationality.objects.filter(name__iexact=tenant_nationality).first()
                    if nat:
                        lead.nationality_id = nat.nationality_id
                if tenant_address is not None:
                    lead.address = tenant_address
                if date_of_birth is not None:
                    lead.date_of_birth = date_of_birth
                if gender is not None:
                    lead.gender = gender
                if marital_status is not None:
                    lead.marital_status = marital_status
                if emergency_contact_name is not None:
                    lead.emergency_contact_name = emergency_contact_name
                if emergency_contact_number is not None:
                    lead.emergency_contact_number = emergency_contact_number
                if profession is not None:
                    lead.profession = profession
                if company_name is not None:
                    lead.company_name = company_name
                lead.save()

                user = User.objects.filter(user_id=check_out.tenant_id).first()
                if user:
                    if tenant_mobile_number is not None:
                        user.phone_number = tenant_mobile_number
                    if tenant_email is not None:
                        user.email = tenant_email
                    user.save()

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
        property_assignment_id: int = None,
        updated_by: int = None,
    ) -> int:
        from pms_apps.property.models.property_details import PropertyDetail
        from pms_apps.property.models.property import Property as PropertyModel
        from pms_apps.property.models.property_assignment import PropertyAssignment

        try:
            check_out = CheckOut.objects.get(check_out_id=check_out_id)
        except CheckOut.DoesNotExist:
            raise ValueError(f"Invalid Check-Out Id: {check_out_id}")

        if property_assignment_id is not None:
            if not PropertyAssignment.objects.filter(property_assignment_id=property_assignment_id).exists():
                raise ValueError(f"Invalid Property Assignment ID: {property_assignment_id}")
            check_out.property_assignment_id = property_assignment_id

        if check_out.property_id:
            detail = PropertyDetail.objects.filter(property_id=check_out.property_id).first()
            if detail:
                if building_name is not None:
                    detail.building_name = building_name
                if floor_number is not None:
                    try:
                        detail.floor_number = int(floor_number)
                    except (ValueError, TypeError):
                        pass
                if property_status is not None:
                    detail.current_status = property_status
                if flat_unit_number is not None:
                    prop = PropertyModel.objects.filter(property_id=check_out.property_id).values('rental_type').first()
                    rtype = prop.get('rental_type') if prop else None
                    if rtype == 'Flat':
                        detail.flat_number = flat_unit_number
                    elif rtype == 'Commercial':
                        detail.commercial_category = flat_unit_number
                    elif rtype == 'Villa':
                        detail.villa_name = flat_unit_number
                detail.save()

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
        inspection_duration: str = None,
        manager_approval: str = None,
        inspection_priority: str = None,
        issue_identified: str = None,
        supervisor_remarks: str = None,
        next_inspection_due=None,
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
        if inspection_duration is not None:
            check_out.inspection_duration = inspection_duration
        if manager_approval is not None:
            check_out.manager_approval = manager_approval
        if inspection_priority is not None:
            check_out.inspection_priority = inspection_priority
        if issue_identified is not None:
            check_out.issue_identified = issue_identified
        if supervisor_remarks is not None:
            check_out.supervisor_remarks = supervisor_remarks
        if next_inspection_due is not None:
            check_out.next_inspection_due = next_inspection_due
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
        repair_priority: str = None,
        recommended_by_id: int = None,
        approved_by_id: int = None,
        approved_on=None,
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
        if repair_priority is not None:
            check_out.repair_priority = repair_priority
        if recommended_by_id is not None:
            check_out.recommended_by_id = recommended_by_id
        if approved_by_id is not None:
            check_out.approved_by_id = approved_by_id
        if approved_on is not None:
            check_out.approved_on = approved_on
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
        settlement_status: str = None,
        finance_description: str = None,
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
        if settlement_status is not None:
            check_out.settlement_status = settlement_status
        if finance_description is not None:
            check_out.finance_description = finance_description
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
        key_type: str = None,
        key_available: str = None,
        key_return: str = None,
        expected_return_date=None,
        key_booking_date=None,
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
        if key_type is not None:
            check_out.key_type = key_type
        if key_available is not None:
            check_out.key_available = key_available
        if key_return is not None:
            check_out.key_return = key_return
        if expected_return_date is not None:
            check_out.expected_return_date = expected_return_date
        if key_booking_date is not None:
            check_out.key_booking_date = key_booking_date
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
