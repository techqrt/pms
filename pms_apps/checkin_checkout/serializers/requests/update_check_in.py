from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_in import CheckIn
from pms_apps.checkin_checkout.dataclasses.requests.update_check_in import (
    CheckInInformationUpdateRequest,
    CheckInTenantDetailsUpdateRequest,
    CheckInPropertyDetailsUpdateRequest,
    CheckInRentalDetailsUpdateRequest,
    CheckInPropertyInspectionUpdateRequest,
    CheckInRepairApprovalUpdateRequest,
    CheckInUtilityMeterReadingsUpdateRequest,
    CheckInAgreementDetailsUpdateRequest,
    CheckInKeyHandoverUpdateRequest,
    CheckInCommentsUpdateRequest,
)


def _choices(choice_list):
    return [choice[0] for choice in choice_list]


class CheckInInformationUpdateSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()
    assigned_employee_id = serializers.IntegerField(required=False, allow_null=True)
    check_in_date = serializers.DateField(required=False, allow_null=True)
    check_in_status = serializers.ChoiceField(
        choices=_choices(CheckIn.CHECK_IN_STATUS_CHOICES), required=False, allow_null=True
    )
    remarks_notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def create(self, validated_data) -> CheckInInformationUpdateRequest:
        return CheckInInformationUpdateRequest(**validated_data)


class CheckInTenantDetailsUpdateSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()
    tenant_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tenant_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tenant_type = serializers.ChoiceField(
        choices=_choices(CheckIn.TENANT_TYPE_CHOICES), required=False, allow_null=True
    )
    tenant_mobile_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tenant_email = serializers.EmailField(required=False, allow_null=True)
    tenant_civil_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tenant_passport_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tenant_nationality = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tenant_address = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    gender = serializers.ChoiceField(
        choices=_choices(CheckIn.GENDER_CHOICES), required=False, allow_null=True
    )
    marital_status = serializers.ChoiceField(
        choices=_choices(CheckIn.MARITAL_STATUS_CHOICES), required=False, allow_null=True
    )
    alternate_mobile_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    emergency_contact_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    emergency_contact_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    profession = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    company_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    move_in_reason = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    number_of_occupants = serializers.IntegerField(required=False, allow_null=True)

    def create(self, validated_data) -> CheckInTenantDetailsUpdateRequest:
        return CheckInTenantDetailsUpdateRequest(**validated_data)


class CheckInPropertyDetailsUpdateSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()
    property_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    property_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    building_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    flat_unit_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    floor_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    property_status = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def create(self, validated_data) -> CheckInPropertyDetailsUpdateRequest:
        return CheckInPropertyDetailsUpdateRequest(**validated_data)


class CheckInRentalDetailsUpdateSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()
    monthly_rent = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    security_deposit = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    advance_rent_received = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    first_month_rent_paid = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    payment_mode = serializers.ChoiceField(
        choices=_choices(CheckIn.PAYMENT_MODE_CHOICES), required=False, allow_null=True
    )
    maintenance_charges = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)

    def create(self, validated_data) -> CheckInRentalDetailsUpdateRequest:
        return CheckInRentalDetailsUpdateRequest(**validated_data)


class CheckInPropertyInspectionUpdateSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()
    inspection_required = serializers.ChoiceField(
        choices=_choices(CheckIn.YES_NO_CHOICES), required=False, allow_null=True
    )
    inspection_date = serializers.DateField(required=False, allow_null=True)
    technician_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    manager_approval = serializers.ChoiceField(
        choices=_choices(CheckIn.APPROVAL_STATUS_CHOICES), required=False, allow_null=True
    )
    issue_identified = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    supervisor_remarks = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    inspection_priority = serializers.ChoiceField(
        choices=_choices(CheckIn.PRIORITY_CHOICES), required=False, allow_null=True
    )
    inspection_type = serializers.ChoiceField(
        choices=_choices(CheckIn.INSPECTION_TYPE_CHOICES), required=False, allow_null=True
    )
    inspection_duration = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    next_inspection_due = serializers.DateField(required=False, allow_null=True)

    def create(self, validated_data) -> CheckInPropertyInspectionUpdateRequest:
        return CheckInPropertyInspectionUpdateRequest(**validated_data)


class CheckInRepairApprovalUpdateSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()
    repair_required = serializers.ChoiceField(
        choices=_choices(CheckIn.YES_NO_CHOICES), required=False, allow_null=True
    )
    quotation_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    inventory_available = serializers.ChoiceField(
        choices=_choices(CheckIn.YES_NO_CHOICES), required=False, allow_null=True
    )
    gm_approval = serializers.ChoiceField(
        choices=_choices(CheckIn.APPROVAL_STATUS_CHOICES), required=False, allow_null=True
    )
    landlord_consent = serializers.ChoiceField(
        choices=_choices(CheckIn.APPROVAL_STATUS_CHOICES), required=False, allow_null=True
    )
    finance_alert_generated = serializers.ChoiceField(
        choices=_choices(CheckIn.YES_NO_CHOICES), required=False, allow_null=True
    )
    rent_adjustment_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    repair_priority = serializers.ChoiceField(
        choices=_choices(CheckIn.PRIORITY_CHOICES), required=False, allow_null=True
    )
    recommended_by_id = serializers.IntegerField(required=False, allow_null=True)
    approved_by_id = serializers.IntegerField(required=False, allow_null=True)
    approved_on = serializers.DateField(required=False, allow_null=True)
    inspector_comments = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data) -> CheckInRepairApprovalUpdateRequest:
        return CheckInRepairApprovalUpdateRequest(**validated_data)


class CheckInUtilityMeterReadingsUpdateSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()
    electricity_meter_reading = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    water_meter_reading = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    gas_meter_reading = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    utility_adjustment_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)

    def create(self, validated_data) -> CheckInUtilityMeterReadingsUpdateRequest:
        return CheckInUtilityMeterReadingsUpdateRequest(**validated_data)


class CheckInAgreementDetailsUpdateSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()
    agreement_type = serializers.ChoiceField(
        choices=_choices(CheckIn.AGREEMENT_TYPE_CHOICES), required=False, allow_null=True
    )
    agreement_status = serializers.ChoiceField(
        choices=_choices(CheckIn.AGREEMENT_STATUS_CHOICES), required=False, allow_null=True
    )
    agreement_start_date = serializers.DateField(required=False, allow_null=True)
    agreement_end_date = serializers.DateField(required=False, allow_null=True)
    agreement_document = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    agreement_template = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    agreement_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    generated_on = serializers.DateTimeField(required=False, allow_null=True)
    generated_by_id = serializers.IntegerField(required=False, allow_null=True)
    submitted_to_tenant_on = serializers.DateTimeField(required=False, allow_null=True)
    tenant_signed_on = serializers.DateTimeField(required=False, allow_null=True)
    manager_signed_on = serializers.DateTimeField(required=False, allow_null=True)
    signed_by_id = serializers.IntegerField(required=False, allow_null=True)
    renewal_reminder_date = serializers.DateField(required=False, allow_null=True)
    auto_reminder_enabled = serializers.BooleanField(required=False, allow_null=True)
    agreement_notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def create(self, validated_data) -> CheckInAgreementDetailsUpdateRequest:
        return CheckInAgreementDetailsUpdateRequest(**validated_data)


class CheckInKeyHandoverUpdateSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()
    key_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    key_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    key_available = serializers.ChoiceField(
        choices=_choices(CheckIn.YES_NO_CHOICES), required=False, allow_null=True
    )
    key_booking_date = serializers.DateField(required=False, allow_null=True)
    confirmation_received = serializers.ChoiceField(
        choices=_choices(CheckIn.YES_NO_CHOICES), required=False, allow_null=True
    )
    key_delivery_date = serializers.DateField(required=False, allow_null=True)
    key_handover_status = serializers.ChoiceField(
        choices=_choices(CheckIn.KEY_HANDOVER_STATUS_CHOICES), required=False, allow_null=True
    )
    expected_handover_date = serializers.DateTimeField(required=False, allow_null=True)
    handover_notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tenant_confirmation_notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    key_booked_on = serializers.DateTimeField(required=False, allow_null=True)
    key_booked_by_id = serializers.IntegerField(required=False, allow_null=True)
    key_prepared_on = serializers.DateTimeField(required=False, allow_null=True)
    key_notified_on = serializers.DateTimeField(required=False, allow_null=True)
    handover_completed_on = serializers.DateTimeField(required=False, allow_null=True)
    handed_over_by_id = serializers.IntegerField(required=False, allow_null=True)

    def create(self, validated_data) -> CheckInKeyHandoverUpdateRequest:
        return CheckInKeyHandoverUpdateRequest(**validated_data)


class CheckInCommentsUpdateSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()
    internal_comments = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tenant_remarks = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    special_instructions = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def create(self, validated_data) -> CheckInCommentsUpdateRequest:
        return CheckInCommentsUpdateRequest(**validated_data)
