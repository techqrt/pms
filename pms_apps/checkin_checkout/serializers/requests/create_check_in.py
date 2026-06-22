from rest_framework import serializers
from pms_apps.checkin_checkout.dataclasses.requests.create_check_in import CheckInCreateRequest
from pms_apps.checkin_checkout.models.check_in import CheckIn


class CheckInCreateSerializer(serializers.Serializer):
    property_id = serializers.IntegerField()
    property_assignment_id = serializers.IntegerField(required=False, allow_null=True)
    tenant_id = serializers.IntegerField(required=False, allow_null=True)
    assigned_employee_id = serializers.IntegerField(required=False, allow_null=True)

    # A. Check-In Information
    check_in_date = serializers.DateField(required=False, allow_null=True)
    check_in_status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.CHECK_IN_STATUS_CHOICES],
        default="Pending"
    )
    remarks_notes = serializers.CharField(required=False, default="", allow_blank=True)

    # B. Tenant Details
    tenant_code = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tenant_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tenant_type = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.TENANT_TYPE_CHOICES],
        required=False, allow_null=True
    )
    tenant_mobile_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tenant_email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    tenant_civil_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tenant_passport_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tenant_nationality = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tenant_address = serializers.CharField(required=False, default="", allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    gender = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.GENDER_CHOICES],
        required=False, allow_null=True
    )
    marital_status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.MARITAL_STATUS_CHOICES],
        required=False, allow_null=True
    )
    alternate_mobile_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    emergency_contact_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    emergency_contact_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    profession = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    company_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    move_in_reason = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    number_of_occupants = serializers.IntegerField(required=False, allow_null=True)

    # C. Property Details
    property_type = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    property_code = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    building_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    flat_unit_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    floor_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    property_status = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    # D. Rental Details
    monthly_rent = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    security_deposit = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    advance_rent_received = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    first_month_rent_paid = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    payment_mode = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.PAYMENT_MODE_CHOICES],
        required=False, allow_null=True
    )
    maintenance_charges = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)

    # E. Property Inspection
    inspection_required = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.YES_NO_CHOICES],
        required=False, allow_null=True
    )
    inspection_date = serializers.DateField(required=False, allow_null=True)
    technician_type = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    manager_approval = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.APPROVAL_STATUS_CHOICES],
        required=False, allow_null=True
    )
    issue_identified = serializers.CharField(required=False, default="", allow_blank=True)
    supervisor_remarks = serializers.CharField(required=False, default="", allow_blank=True)
    inspection_priority = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.PRIORITY_CHOICES],
        required=False, allow_null=True
    )
    inspection_type = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.INSPECTION_TYPE_CHOICES],
        required=False, allow_null=True
    )
    inspection_duration = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    next_inspection_due = serializers.DateField(required=False, allow_null=True)

    # F. Repair & Approval
    repair_required = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.YES_NO_CHOICES],
        required=False, allow_null=True
    )
    quotation_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    inventory_available = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.YES_NO_CHOICES],
        required=False, allow_null=True
    )
    gm_approval = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.APPROVAL_STATUS_CHOICES],
        required=False, allow_null=True
    )
    landlord_consent = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.APPROVAL_STATUS_CHOICES],
        required=False, allow_null=True
    )
    finance_alert_generated = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.YES_NO_CHOICES],
        required=False, allow_null=True
    )
    rent_adjustment_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    repair_priority = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.PRIORITY_CHOICES],
        required=False, allow_null=True
    )
    recommended_by_id = serializers.IntegerField(required=False, allow_null=True)
    approved_by_id = serializers.IntegerField(required=False, allow_null=True)
    approved_on = serializers.DateField(required=False, allow_null=True)
    inspector_comments = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    # G. Utility Meter Readings
    electricity_meter_reading = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    water_meter_reading = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    gas_meter_reading = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    utility_adjustment_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)

    # H. Agreement Details
    agreement_type = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.AGREEMENT_TYPE_CHOICES],
        required=False, allow_null=True
    )
    agreement_status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.AGREEMENT_STATUS_CHOICES],
        default="Pending"
    )
    agreement_start_date = serializers.DateField(required=False, allow_null=True)
    agreement_end_date = serializers.DateField(required=False, allow_null=True)
    agreement_document = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    agreement_template = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    agreement_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    generated_on = serializers.DateTimeField(required=False, allow_null=True)
    generated_by_id = serializers.IntegerField(required=False, allow_null=True)
    submitted_to_tenant_on = serializers.DateTimeField(required=False, allow_null=True)
    tenant_signed_on = serializers.DateTimeField(required=False, allow_null=True)
    manager_signed_on = serializers.DateTimeField(required=False, allow_null=True)
    signed_by_id = serializers.IntegerField(required=False, allow_null=True)
    renewal_reminder_date = serializers.DateField(required=False, allow_null=True)
    auto_reminder_enabled = serializers.BooleanField(required=False, allow_null=True)
    agreement_notes = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    # I. Key Handover
    key_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    key_type = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    key_available = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.YES_NO_CHOICES],
        required=False, allow_null=True
    )
    key_booking_date = serializers.DateField(required=False, allow_null=True)
    confirmation_received = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.YES_NO_CHOICES],
        required=False, allow_null=True
    )
    key_delivery_date = serializers.DateField(required=False, allow_null=True)
    key_handover_status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckIn.KEY_HANDOVER_STATUS_CHOICES],
        default="Pending"
    )
    expected_handover_date = serializers.DateTimeField(required=False, allow_null=True)
    handover_notes = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tenant_confirmation_notes = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    key_booked_on = serializers.DateTimeField(required=False, allow_null=True)
    key_booked_by_id = serializers.IntegerField(required=False, allow_null=True)
    key_prepared_on = serializers.DateTimeField(required=False, allow_null=True)
    key_notified_on = serializers.DateTimeField(required=False, allow_null=True)
    handover_completed_on = serializers.DateTimeField(required=False, allow_null=True)
    handed_over_by_id = serializers.IntegerField(required=False, allow_null=True)

    # K. Comments
    internal_comments = serializers.CharField(required=False, default="", allow_blank=True)
    tenant_remarks = serializers.CharField(required=False, default="", allow_blank=True)
    special_instructions = serializers.CharField(required=False, default="", allow_blank=True)

    # M. Activity Timeline
    property_created_date = serializers.DateField(required=False, allow_null=True)
    listed_for_rent_date = serializers.DateField(required=False, allow_null=True)
    tenant_assigned_date = serializers.DateField(required=False, allow_null=True)
    assigned_to_employee_date = serializers.DateField(required=False, allow_null=True)
    property_occupied_date = serializers.DateField(required=False, allow_null=True)

    def create(self, validated_data) -> CheckInCreateRequest:
        return CheckInCreateRequest(
            property_id=validated_data['property_id'],
            property_assignment_id=validated_data.get('property_assignment_id'),
            tenant_id=validated_data.get('tenant_id'),
            assigned_employee_id=validated_data.get('assigned_employee_id'),

            check_in_date=validated_data.get('check_in_date'),
            check_in_status=validated_data.get('check_in_status', 'Pending'),
            remarks_notes=validated_data.get('remarks_notes', ''),

            tenant_code=validated_data.get('tenant_code'),
            tenant_name=validated_data.get('tenant_name'),
            tenant_type=validated_data.get('tenant_type'),
            tenant_mobile_number=validated_data.get('tenant_mobile_number'),
            tenant_email=validated_data.get('tenant_email'),
            tenant_civil_id=validated_data.get('tenant_civil_id'),
            tenant_passport_number=validated_data.get('tenant_passport_number'),
            tenant_nationality=validated_data.get('tenant_nationality'),
            tenant_address=validated_data.get('tenant_address', ''),
            date_of_birth=validated_data.get('date_of_birth'),
            gender=validated_data.get('gender'),
            marital_status=validated_data.get('marital_status'),
            alternate_mobile_number=validated_data.get('alternate_mobile_number'),
            emergency_contact_name=validated_data.get('emergency_contact_name'),
            emergency_contact_number=validated_data.get('emergency_contact_number'),
            profession=validated_data.get('profession'),
            company_name=validated_data.get('company_name'),
            move_in_reason=validated_data.get('move_in_reason'),
            number_of_occupants=validated_data.get('number_of_occupants'),

            property_type=validated_data.get('property_type'),
            property_code=validated_data.get('property_code'),
            building_name=validated_data.get('building_name'),
            flat_unit_number=validated_data.get('flat_unit_number'),
            floor_number=validated_data.get('floor_number'),
            property_status=validated_data.get('property_status'),

            monthly_rent=validated_data.get('monthly_rent'),
            security_deposit=validated_data.get('security_deposit'),
            advance_rent_received=validated_data.get('advance_rent_received'),
            first_month_rent_paid=validated_data.get('first_month_rent_paid'),
            payment_mode=validated_data.get('payment_mode'),
            maintenance_charges=validated_data.get('maintenance_charges'),

            inspection_required=validated_data.get('inspection_required'),
            inspection_date=validated_data.get('inspection_date'),
            technician_type=validated_data.get('technician_type'),
            manager_approval=validated_data.get('manager_approval'),
            issue_identified=validated_data.get('issue_identified', ''),
            supervisor_remarks=validated_data.get('supervisor_remarks', ''),
            inspection_priority=validated_data.get('inspection_priority'),
            inspection_type=validated_data.get('inspection_type'),
            inspection_duration=validated_data.get('inspection_duration'),
            next_inspection_due=validated_data.get('next_inspection_due'),

            repair_required=validated_data.get('repair_required'),
            quotation_amount=validated_data.get('quotation_amount'),
            inventory_available=validated_data.get('inventory_available'),
            gm_approval=validated_data.get('gm_approval'),
            landlord_consent=validated_data.get('landlord_consent'),
            finance_alert_generated=validated_data.get('finance_alert_generated'),
            rent_adjustment_amount=validated_data.get('rent_adjustment_amount'),
            repair_priority=validated_data.get('repair_priority'),
            recommended_by_id=validated_data.get('recommended_by_id'),
            approved_by_id=validated_data.get('approved_by_id'),
            approved_on=validated_data.get('approved_on'),
            inspector_comments=validated_data.get('inspector_comments'),

            electricity_meter_reading=validated_data.get('electricity_meter_reading'),
            water_meter_reading=validated_data.get('water_meter_reading'),
            gas_meter_reading=validated_data.get('gas_meter_reading'),
            utility_adjustment_amount=validated_data.get('utility_adjustment_amount'),

            agreement_type=validated_data.get('agreement_type'),
            agreement_status=validated_data.get('agreement_status', 'Pending'),
            agreement_start_date=validated_data.get('agreement_start_date'),
            agreement_end_date=validated_data.get('agreement_end_date'),
            agreement_document=validated_data.get('agreement_document'),
            agreement_template=validated_data.get('agreement_template'),
            agreement_number=validated_data.get('agreement_number'),
            generated_on=validated_data.get('generated_on'),
            generated_by_id=validated_data.get('generated_by_id'),
            submitted_to_tenant_on=validated_data.get('submitted_to_tenant_on'),
            tenant_signed_on=validated_data.get('tenant_signed_on'),
            manager_signed_on=validated_data.get('manager_signed_on'),
            signed_by_id=validated_data.get('signed_by_id'),
            renewal_reminder_date=validated_data.get('renewal_reminder_date'),
            auto_reminder_enabled=validated_data.get('auto_reminder_enabled'),
            agreement_notes=validated_data.get('agreement_notes'),

            key_number=validated_data.get('key_number'),
            key_type=validated_data.get('key_type'),
            key_available=validated_data.get('key_available'),
            key_booking_date=validated_data.get('key_booking_date'),
            confirmation_received=validated_data.get('confirmation_received'),
            key_delivery_date=validated_data.get('key_delivery_date'),
            key_handover_status=validated_data.get('key_handover_status', 'Pending'),
            expected_handover_date=validated_data.get('expected_handover_date'),
            handover_notes=validated_data.get('handover_notes'),
            tenant_confirmation_notes=validated_data.get('tenant_confirmation_notes'),
            key_booked_on=validated_data.get('key_booked_on'),
            key_booked_by_id=validated_data.get('key_booked_by_id'),
            key_prepared_on=validated_data.get('key_prepared_on'),
            key_notified_on=validated_data.get('key_notified_on'),
            handover_completed_on=validated_data.get('handover_completed_on'),
            handed_over_by_id=validated_data.get('handed_over_by_id'),

            internal_comments=validated_data.get('internal_comments', ''),
            tenant_remarks=validated_data.get('tenant_remarks', ''),
            special_instructions=validated_data.get('special_instructions', ''),

            property_created_date=validated_data.get('property_created_date'),
            listed_for_rent_date=validated_data.get('listed_for_rent_date'),
            tenant_assigned_date=validated_data.get('tenant_assigned_date'),
            assigned_to_employee_date=validated_data.get('assigned_to_employee_date'),
            property_occupied_date=validated_data.get('property_occupied_date'),
        )
