from rest_framework import serializers
from pms_apps.checkin_checkout.dataclasses.requests.create_check_out import CheckOutCreateRequest
from pms_apps.checkin_checkout.models.check_out import CheckOut
from pms_apps.lead.models.lead import Lead


class CheckOutCreateSerializer(serializers.Serializer):
    property_id = serializers.IntegerField()
    property_assignment_id = serializers.IntegerField(required=False, allow_null=True)
    check_in_id = serializers.IntegerField(required=False, allow_null=True)
    tenant_id = serializers.IntegerField(required=False, allow_null=True)
    assigned_employee_id = serializers.IntegerField(required=False, allow_null=True)

    # A. Check-Out Information
    check_out_date = serializers.DateField(required=False, allow_null=True)
    check_out_status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOut.CHECK_OUT_STATUS_CHOICES],
        default="Pending"
    )
    remarks_notes = serializers.CharField(required=False, default="", allow_blank=True)

    # B. Tenant Details
    tenant_code = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tenant_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tenant_type = serializers.ChoiceField(
        choices=[choice[0] for choice in Lead.TENANT_TYPE_CHOICES],
        required=False, allow_null=True
    )
    tenant_mobile_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tenant_email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    tenant_civil_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tenant_passport_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tenant_nationality = serializers.CharField(required=False, allow_null=True, allow_blank=True)

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
        choices=[choice[0] for choice in CheckOut.PAYMENT_MODE_CHOICES],
        required=False, allow_null=True
    )
    maintenance_charges = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)

    # E. Property Inspection
    inspection_required = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOut.YES_NO_CHOICES],
        required=False, allow_null=True
    )
    inspection_date = serializers.DateField(required=False, allow_null=True)
    technician_type = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    manager_approval = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOut.APPROVAL_STATUS_CHOICES],
        required=False, allow_null=True
    )
    issue_identified = serializers.CharField(required=False, default="", allow_blank=True)
    supervisor_remarks = serializers.CharField(required=False, default="", allow_blank=True)

    # F. Repair & Damage
    repair_required = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOut.YES_NO_CHOICES],
        required=False, allow_null=True
    )
    quotation_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    inventory_available = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOut.YES_NO_CHOICES],
        required=False, allow_null=True
    )
    gm_approval = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOut.APPROVAL_STATUS_CHOICES],
        required=False, allow_null=True
    )
    landlord_consent = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOut.APPROVAL_STATUS_CHOICES],
        required=False, allow_null=True
    )
    finance_alert_generated = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOut.YES_NO_CHOICES],
        required=False, allow_null=True
    )
    rent_adjustment_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)

    # G. Check-Out Utility Meter Readings
    electricity_meter_reading = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    water_meter_reading = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    gas_meter_reading = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)

    # H. Finance Details
    charge_type = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOut.CHARGE_TYPE_CHOICES],
        required=False, allow_null=True
    )
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    payment_status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOut.PAYMENT_STATUS_CHOICES],
        required=False, allow_null=True
    )
    payment_date = serializers.DateField(required=False, allow_null=True)
    transaction_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    payment_proof = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    # I. Key Return
    key_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    key_return = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOut.YES_NO_CHOICES],
        required=False, allow_null=True
    )
    expected_return_date = serializers.DateField(required=False, allow_null=True)
    confirmation_received = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOut.YES_NO_CHOICES],
        required=False, allow_null=True
    )
    key_return_date = serializers.DateField(required=False, allow_null=True)
    key_return_status = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOut.KEY_RETURN_STATUS_CHOICES],
        default="Pending"
    )

    # K. Comments
    internal_comments = serializers.CharField(required=False, default="", allow_blank=True)
    tenant_remarks = serializers.CharField(required=False, default="", allow_blank=True)
    special_instructions = serializers.CharField(required=False, default="", allow_blank=True)

    def create(self, validated_data) -> CheckOutCreateRequest:
        return CheckOutCreateRequest(
            property_id=validated_data['property_id'],
            property_assignment_id=validated_data.get('property_assignment_id'),
            check_in_id=validated_data.get('check_in_id'),
            tenant_id=validated_data.get('tenant_id'),
            assigned_employee_id=validated_data.get('assigned_employee_id'),

            check_out_date=validated_data.get('check_out_date'),
            check_out_status=validated_data.get('check_out_status', 'Pending'),
            remarks_notes=validated_data.get('remarks_notes', ''),

            tenant_code=validated_data.get('tenant_code'),
            tenant_name=validated_data.get('tenant_name'),
            tenant_type=validated_data.get('tenant_type'),
            tenant_mobile_number=validated_data.get('tenant_mobile_number'),
            tenant_email=validated_data.get('tenant_email'),
            tenant_civil_id=validated_data.get('tenant_civil_id'),
            tenant_passport_number=validated_data.get('tenant_passport_number'),
            tenant_nationality=validated_data.get('tenant_nationality'),

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

            repair_required=validated_data.get('repair_required'),
            quotation_amount=validated_data.get('quotation_amount'),
            inventory_available=validated_data.get('inventory_available'),
            gm_approval=validated_data.get('gm_approval'),
            landlord_consent=validated_data.get('landlord_consent'),
            finance_alert_generated=validated_data.get('finance_alert_generated'),
            rent_adjustment_amount=validated_data.get('rent_adjustment_amount'),

            electricity_meter_reading=validated_data.get('electricity_meter_reading'),
            water_meter_reading=validated_data.get('water_meter_reading'),
            gas_meter_reading=validated_data.get('gas_meter_reading'),

            charge_type=validated_data.get('charge_type'),
            total_amount=validated_data.get('total_amount'),
            payment_status=validated_data.get('payment_status'),
            payment_date=validated_data.get('payment_date'),
            transaction_id=validated_data.get('transaction_id'),
            payment_proof=validated_data.get('payment_proof'),

            key_number=validated_data.get('key_number'),
            key_return=validated_data.get('key_return'),
            expected_return_date=validated_data.get('expected_return_date'),
            confirmation_received=validated_data.get('confirmation_received'),
            key_return_date=validated_data.get('key_return_date'),
            key_return_status=validated_data.get('key_return_status', 'Pending'),

            internal_comments=validated_data.get('internal_comments', ''),
            tenant_remarks=validated_data.get('tenant_remarks', ''),
            special_instructions=validated_data.get('special_instructions', ''),
        )
