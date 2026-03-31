from django.db import models
from django.utils import timezone


class PropertyAssignment(models.Model):
    ASSIGNMENT_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Active", "Active"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    AGREEMENT_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Prepared", "Prepared"),
        ("Signed", "Signed"),
        ("Executed", "Executed"),
        ("Terminated", "Terminated"),
    ]

    FINANCE_APPROVAL_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("On Hold", "On Hold"),
        ("Rejected", "Rejected"),
    ]

    MAINTENANCE_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Not Required", "Not Required"),
    ]

    KEY_HANDOVER_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Handed Over", "Handed Over"),
        ("Returned", "Returned"),
    ]

    TENANT_TYPE_CHOICES = [
        ("Individual", "Individual"),
        ("Corporate", "Corporate"),
    ]

    PAYMENT_MODE_CHOICES = [
        ("Cash", "Cash"),
        ("Cheque", "Cheque"),
        ("UPI", "UPI"),
        ("Bank Transfer", "Bank Transfer"),
        ("Card", "Card"),
    ]

    property_assignment_id = models.AutoField(primary_key=True)
    property = models.ForeignKey(
        "property.Property",
        on_delete=models.CASCADE,
        related_name="assignments"
    )
    tenant = models.ForeignKey(
        "lead.Lead",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="property_assignments"
    )
    assigned_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="property_assignments_created"
    )

    # Assignment Status
    assignment_status = models.CharField(
        max_length=20,
        choices=ASSIGNMENT_STATUS_CHOICES,
        default="Pending"
    )

    # Tenant Details
    tenant_type = models.CharField(
        max_length=20,
        choices=TENANT_TYPE_CHOICES,
        default="Individual"
    )
    company_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    # Rental Details
    rental_start_date = models.DateField(null=True, blank=True)
    rental_end_date = models.DateField(null=True, blank=True)
    agreement_duration_months = models.PositiveIntegerField(null=True, blank=True)
    maintenance_charges = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    advance_rent_paid = models.BooleanField(default=False)
    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE_CHOICES,
        null=True,
        blank=True
    )

    # Agreement Details
    agreement_type = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    agreement_status = models.CharField(
        max_length=20,
        choices=AGREEMENT_STATUS_CHOICES,
        default="Pending"
    )
    agreement_prepared_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="agreements_prepared"
    )
    agreement_document = models.FileField(
        upload_to='property/agreements/',
        null=True,
        blank=True
    )

    # Key Management
    key_available_in_office = models.BooleanField(default=False)
    key_code = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    key_handover_date = models.DateField(null=True, blank=True)
    key_handover_status = models.CharField(
        max_length=20,
        choices=KEY_HANDOVER_STATUS_CHOICES,
        default="Pending"
    )

    # Utility Details
    electricity_meter_number = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    electricity_meter_reading_start = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    water_meter_reading_start = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    gas_meter_reading_start = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Financial Approval
    finance_approval_status = models.CharField(
        max_length=20,
        choices=FINANCE_APPROVAL_STATUS_CHOICES,
        default="Pending"
    )
    rent_entry_created = models.BooleanField(default=False)
    invoice_generated = models.BooleanField(default=False)

    # Maintenance Check
    maintenance_required = models.BooleanField(default=False)
    maintenance_ticket_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    maintenance_status = models.CharField(
        max_length=20,
        choices=MAINTENANCE_STATUS_CHOICES,
        default="Pending"
    )

    # Internal Tracking
    internal_notes = models.TextField(blank=True, default="")
    tenant_special_requirements = models.TextField(blank=True, default="")

    # Timestamps
    assigned_on = models.DateTimeField(auto_now_add=True)
    unassigned_on = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Soft Delete
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "property_assignment"
        ordering = ["-assigned_on"]

    def __str__(self):
        return f"Assignment {self.property_assignment_id} - Property {self.property.property_id} - Tenant {self.tenant.lead_id if self.tenant else 'N/A'}"

    @staticmethod
    def create(
        property_id: int,
        tenant_id: int,
        assigned_by_id: int,
        assignment_status: str = "Pending",
        tenant_type: str = "Individual",
        company_name: str = None,
        rental_start_date = None,
        rental_end_date = None,
        agreement_duration_months: int = None,
        maintenance_charges = None,
        advance_rent_paid: bool = False,
        payment_mode: str = None,
        agreement_type: str = None,
        agreement_status: str = "Pending",
        agreement_prepared_by_id: int = None,
        key_available_in_office: bool = False,
        key_code: str = None,
        key_handover_date = None,
        key_handover_status: str = "Pending",
        electricity_meter_number: str = None,
        electricity_meter_reading_start = None,
        water_meter_reading_start = None,
        gas_meter_reading_start = None,
        finance_approval_status: str = "Pending",
        rent_entry_created: bool = False,
        invoice_generated: bool = False,
        maintenance_required: bool = False,
        maintenance_ticket_id: str = None,
        maintenance_status: str = "Pending",
        internal_notes: str = "",
        tenant_special_requirements: str = "",
    ) -> int:
        assignment = PropertyAssignment()
        assignment.property_id = property_id
        assignment.tenant_id = tenant_id
        assignment.assigned_by_id = assigned_by_id
        assignment.assignment_status = assignment_status
        assignment.tenant_type = tenant_type
        assignment.company_name = company_name
        assignment.rental_start_date = rental_start_date
        assignment.rental_end_date = rental_end_date
        assignment.agreement_duration_months = agreement_duration_months
        assignment.maintenance_charges = maintenance_charges
        assignment.advance_rent_paid = advance_rent_paid
        assignment.payment_mode = payment_mode
        assignment.agreement_type = agreement_type
        assignment.agreement_status = agreement_status
        assignment.agreement_prepared_by_id = agreement_prepared_by_id
        assignment.key_available_in_office = key_available_in_office
        assignment.key_code = key_code
        assignment.key_handover_date = key_handover_date
        assignment.key_handover_status = key_handover_status
        assignment.electricity_meter_number = electricity_meter_number
        assignment.electricity_meter_reading_start = electricity_meter_reading_start
        assignment.water_meter_reading_start = water_meter_reading_start
        assignment.gas_meter_reading_start = gas_meter_reading_start
        assignment.finance_approval_status = finance_approval_status
        assignment.rent_entry_created = rent_entry_created
        assignment.invoice_generated = invoice_generated
        assignment.maintenance_required = maintenance_required
        assignment.maintenance_ticket_id = maintenance_ticket_id
        assignment.maintenance_status = maintenance_status
        assignment.internal_notes = internal_notes
        assignment.tenant_special_requirements = tenant_special_requirements

        assignment.save()
        return assignment.property_assignment_id

    @staticmethod
    def update(
        property_assignment_id: int,
        assignment_status: str = None,
        tenant_type: str = None,
        company_name: str = None,
        rental_start_date = None,
        rental_end_date = None,
        agreement_duration_months: int = None,
        maintenance_charges = None,
        advance_rent_paid: bool = None,
        payment_mode: str = None,
        agreement_type: str = None,
        agreement_status: str = None,
        agreement_prepared_by_id: int = None,
        key_available_in_office: bool = None,
        key_code: str = None,
        key_handover_date = None,
        key_handover_status: str = None,
        electricity_meter_number: str = None,
        electricity_meter_reading_start = None,
        water_meter_reading_start = None,
        gas_meter_reading_start = None,
        finance_approval_status: str = None,
        rent_entry_created: bool = None,
        invoice_generated: bool = None,
        maintenance_required: bool = None,
        maintenance_ticket_id: str = None,
        maintenance_status: str = None,
        internal_notes: str = None,
        tenant_special_requirements: str = None,
    ) -> int:
        try:
            assignment = PropertyAssignment.objects.get(property_assignment_id=property_assignment_id)
        except PropertyAssignment.DoesNotExist:
            raise ValueError(f"Invalid Property Assignment Id: {property_assignment_id}")

        if assignment_status is not None:
            assignment.assignment_status = assignment_status
        if tenant_type is not None:
            assignment.tenant_type = tenant_type
        if company_name is not None:
            assignment.company_name = company_name
        if rental_start_date is not None:
            assignment.rental_start_date = rental_start_date
        if rental_end_date is not None:
            assignment.rental_end_date = rental_end_date
        if agreement_duration_months is not None:
            assignment.agreement_duration_months = agreement_duration_months
        if maintenance_charges is not None:
            assignment.maintenance_charges = maintenance_charges
        if advance_rent_paid is not None:
            assignment.advance_rent_paid = advance_rent_paid
        if payment_mode is not None:
            assignment.payment_mode = payment_mode
        if agreement_type is not None:
            assignment.agreement_type = agreement_type
        if agreement_status is not None:
            assignment.agreement_status = agreement_status
        if agreement_prepared_by_id is not None:
            assignment.agreement_prepared_by_id = agreement_prepared_by_id
        if key_available_in_office is not None:
            assignment.key_available_in_office = key_available_in_office
        if key_code is not None:
            assignment.key_code = key_code
        if key_handover_date is not None:
            assignment.key_handover_date = key_handover_date
        if key_handover_status is not None:
            assignment.key_handover_status = key_handover_status
        if electricity_meter_number is not None:
            assignment.electricity_meter_number = electricity_meter_number
        if electricity_meter_reading_start is not None:
            assignment.electricity_meter_reading_start = electricity_meter_reading_start
        if water_meter_reading_start is not None:
            assignment.water_meter_reading_start = water_meter_reading_start
        if gas_meter_reading_start is not None:
            assignment.gas_meter_reading_start = gas_meter_reading_start
        if finance_approval_status is not None:
            assignment.finance_approval_status = finance_approval_status
        if rent_entry_created is not None:
            assignment.rent_entry_created = rent_entry_created
        if invoice_generated is not None:
            assignment.invoice_generated = invoice_generated
        if maintenance_required is not None:
            assignment.maintenance_required = maintenance_required
        if maintenance_ticket_id is not None:
            assignment.maintenance_ticket_id = maintenance_ticket_id
        if maintenance_status is not None:
            assignment.maintenance_status = maintenance_status
        if internal_notes is not None:
            assignment.internal_notes = internal_notes
        if tenant_special_requirements is not None:
            assignment.tenant_special_requirements = tenant_special_requirements

        assignment.save()
        return assignment.property_assignment_id

    @staticmethod
    def get(property_assignment_id: int):
        """Get assignment by ID."""
        try:
            return PropertyAssignment.objects.filter(
                property_assignment_id=property_assignment_id,
                is_active=True
            ).values(
                'property_assignment_id',
                'property_id',
                'tenant__lead_id',
                'tenant__user__name',
                'tenant__user__phone_number',
                'tenant__user__email',
                'assigned_by__user_id',
                'assigned_by__name',
                'assignment_status',
                'tenant_type',
                'company_name',
                'rental_start_date',
                'rental_end_date',
                'agreement_duration_months',
                'maintenance_charges',
                'advance_rent_paid',
                'payment_mode',
                'agreement_type',
                'agreement_status',
                'agreement_prepared_by__name',
                'key_available_in_office',
                'key_code',
                'key_handover_date',
                'key_handover_status',
                'electricity_meter_number',
                'electricity_meter_reading_start',
                'water_meter_reading_start',
                'gas_meter_reading_start',
                'finance_approval_status',
                'rent_entry_created',
                'invoice_generated',
                'maintenance_required',
                'maintenance_ticket_id',
                'maintenance_status',
                'internal_notes',
                'tenant_special_requirements',
                'assigned_on',
                'unassigned_on',
                'created_at'
            ).first()
        except PropertyAssignment.DoesNotExist:
            return None

    @staticmethod
    def get_all_by_property(property_id: int):
        """Get all assignments for a property."""
        return list(PropertyAssignment.objects.filter(
            property_id=property_id,
            is_active=True
        ).values(
            'property_assignment_id',
            'tenant__lead_id',
            'tenant__user__name',
            'tenant__user__phone_number',
            'assignment_status',
            'tenant_type',
            'rental_start_date',
            'rental_end_date',
            'assigned_on'
        ).order_by('-assigned_on'))

    @staticmethod
    def get_active_assignment(property_id: int):
        """Get current active assignment for a property."""
        return PropertyAssignment.objects.filter(
            property_id=property_id,
            is_active=True,
            assignment_status__in=["Active", "Approved"]
        ).values(
            'property_assignment_id',
            'tenant__lead_id',
            'tenant__user__name',
            'assigned_on'
        ).first()

    @staticmethod
    def delete(property_assignment_id: int):
        """Soft delete assignment."""
        return PropertyAssignment.objects.filter(
            property_assignment_id=property_assignment_id
        ).update(is_active=False, unassigned_on=timezone.now())

    @staticmethod
    def end_assignment(property_assignment_id: int):
        """End/unassign a property assignment."""
        try:
            assignment = PropertyAssignment.objects.get(property_assignment_id=property_assignment_id)
            assignment.assignment_status = "Completed"
            assignment.unassigned_on = timezone.now()
            assignment.save()
            return property_assignment_id
        except PropertyAssignment.DoesNotExist:
            raise ValueError(f"Invalid Property Assignment Id: {property_assignment_id}")
