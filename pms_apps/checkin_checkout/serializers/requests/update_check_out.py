from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_out import CheckOut
from pms_apps.lead.models.lead import Lead
from pms_apps.checkin_checkout.dataclasses.requests.update_check_out import (
    CheckOutInformationUpdateRequest,
    CheckOutTenantDetailsUpdateRequest,
    CheckOutPropertyDetailsUpdateRequest,
    CheckOutRentalDetailsUpdateRequest,
    CheckOutPropertyInspectionUpdateRequest,
    CheckOutRepairDamageUpdateRequest,
    CheckOutUtilityMeterReadingsUpdateRequest,
    CheckOutFinanceDetailsUpdateRequest,
    CheckOutKeyReturnUpdateRequest,
    CheckOutCommentsUpdateRequest,
    CheckOutDocumentsUpdateRequest,
)


def _choices(choice_list):
    return [choice[0] for choice in choice_list]


class CheckOutInformationUpdateSerializer(serializers.Serializer):
    check_out_id = serializers.IntegerField()
    assigned_employee_id = serializers.IntegerField(required=False, allow_null=True)
    check_out_date = serializers.DateField(required=False, allow_null=True)
    check_out_status = serializers.ChoiceField(
        choices=_choices(CheckOut.CHECK_OUT_STATUS_CHOICES), required=False, allow_null=True
    )
    remarks_notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    request_from = serializers.ChoiceField(
        choices=_choices(CheckOut.REQUEST_FROM_CHOICES), required=False, allow_null=True
    )

    def create(self, validated_data) -> CheckOutInformationUpdateRequest:
        return CheckOutInformationUpdateRequest(**validated_data)


class CheckOutTenantDetailsUpdateSerializer(serializers.Serializer):
    check_out_id = serializers.IntegerField()
    tenant_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tenant_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tenant_type = serializers.ChoiceField(
        choices=_choices(Lead.TENANT_TYPE_CHOICES), required=False, allow_null=True
    )
    tenant_mobile_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tenant_email = serializers.EmailField(required=False, allow_null=True)
    tenant_civil_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tenant_passport_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tenant_nationality = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tenant_address = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    gender = serializers.ChoiceField(
        choices=_choices(Lead.GENDER_CHOICES), required=False, allow_null=True
    )
    marital_status = serializers.ChoiceField(
        choices=_choices(Lead.MARITAL_STATUS_CHOICES), required=False, allow_null=True
    )
    emergency_contact_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    emergency_contact_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    profession = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    company_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def create(self, validated_data) -> CheckOutTenantDetailsUpdateRequest:
        return CheckOutTenantDetailsUpdateRequest(**validated_data)


class CheckOutPropertyDetailsUpdateSerializer(serializers.Serializer):
    check_out_id = serializers.IntegerField()
    property_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    property_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    building_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    flat_unit_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    floor_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    property_status = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    property_assignment_id = serializers.IntegerField(required=False, allow_null=True)

    def create(self, validated_data) -> CheckOutPropertyDetailsUpdateRequest:
        return CheckOutPropertyDetailsUpdateRequest(**validated_data)


class CheckOutRentalDetailsUpdateSerializer(serializers.Serializer):
    check_out_id = serializers.IntegerField()
    monthly_rent = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    security_deposit = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    advance_rent_received = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    first_month_rent_paid = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    payment_mode = serializers.ChoiceField(
        choices=_choices(CheckOut.PAYMENT_MODE_CHOICES), required=False, allow_null=True
    )
    maintenance_charges = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)

    def create(self, validated_data) -> CheckOutRentalDetailsUpdateRequest:
        return CheckOutRentalDetailsUpdateRequest(**validated_data)


class CheckOutPropertyInspectionUpdateSerializer(serializers.Serializer):
    check_out_id = serializers.IntegerField()
    inspection_required = serializers.ChoiceField(
        choices=_choices(CheckOut.YES_NO_CHOICES), required=False, allow_null=True
    )
    inspection_date = serializers.DateField(required=False, allow_null=True)
    technician_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    inspection_duration = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    manager_approval = serializers.ChoiceField(
        choices=_choices(CheckOut.APPROVAL_STATUS_CHOICES), required=False, allow_null=True
    )
    inspection_priority = serializers.ChoiceField(
        choices=_choices(CheckOut.PRIORITY_CHOICES), required=False, allow_null=True
    )
    issue_identified = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    supervisor_remarks = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    next_inspection_due = serializers.DateField(required=False, allow_null=True)

    def create(self, validated_data) -> CheckOutPropertyInspectionUpdateRequest:
        return CheckOutPropertyInspectionUpdateRequest(**validated_data)


class CheckOutRepairDamageUpdateSerializer(serializers.Serializer):
    check_out_id = serializers.IntegerField()
    repair_required = serializers.ChoiceField(
        choices=_choices(CheckOut.YES_NO_CHOICES), required=False, allow_null=True
    )
    quotation_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    inventory_available = serializers.ChoiceField(
        choices=_choices(CheckOut.YES_NO_CHOICES), required=False, allow_null=True
    )
    gm_approval = serializers.ChoiceField(
        choices=_choices(CheckOut.APPROVAL_STATUS_CHOICES), required=False, allow_null=True
    )
    landlord_consent = serializers.ChoiceField(
        choices=_choices(CheckOut.APPROVAL_STATUS_CHOICES), required=False, allow_null=True
    )
    finance_alert_generated = serializers.ChoiceField(
        choices=_choices(CheckOut.YES_NO_CHOICES), required=False, allow_null=True
    )
    rent_adjustment_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    repair_priority = serializers.ChoiceField(
        choices=_choices(CheckOut.PRIORITY_CHOICES), required=False, allow_null=True
    )
    recommended_by_id = serializers.IntegerField(required=False, allow_null=True)
    approved_by_id = serializers.IntegerField(required=False, allow_null=True)
    approved_on = serializers.DateField(required=False, allow_null=True)

    def create(self, validated_data) -> CheckOutRepairDamageUpdateRequest:
        return CheckOutRepairDamageUpdateRequest(**validated_data)


class CheckOutUtilityMeterReadingsUpdateSerializer(serializers.Serializer):
    check_out_id = serializers.IntegerField()
    electricity_meter_reading = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    water_meter_reading = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    gas_meter_reading = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)

    def create(self, validated_data) -> CheckOutUtilityMeterReadingsUpdateRequest:
        return CheckOutUtilityMeterReadingsUpdateRequest(**validated_data)


class CheckOutFinanceDetailsUpdateSerializer(serializers.Serializer):
    check_out_id = serializers.IntegerField()
    charge_type = serializers.ChoiceField(
        choices=_choices(CheckOut.CHARGE_TYPE_CHOICES), required=False, allow_null=True
    )
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    payment_status = serializers.ChoiceField(
        choices=_choices(CheckOut.PAYMENT_STATUS_CHOICES), required=False, allow_null=True
    )
    payment_date = serializers.DateField(required=False, allow_null=True)
    transaction_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    settlement_status = serializers.ChoiceField(
        choices=_choices(CheckOut.SETTLEMENT_STATUS_CHOICES), required=False, allow_null=True
    )
    finance_description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    payment_proof = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def create(self, validated_data) -> CheckOutFinanceDetailsUpdateRequest:
        return CheckOutFinanceDetailsUpdateRequest(**validated_data)


class CheckOutKeyReturnUpdateSerializer(serializers.Serializer):
    check_out_id = serializers.IntegerField()
    key_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    key_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    key_available = serializers.ChoiceField(
        choices=_choices(CheckOut.YES_NO_CHOICES), required=False, allow_null=True
    )
    key_return = serializers.ChoiceField(
        choices=_choices(CheckOut.YES_NO_CHOICES), required=False, allow_null=True
    )
    expected_return_date = serializers.DateField(required=False, allow_null=True)
    key_booking_date = serializers.DateField(required=False, allow_null=True)
    confirmation_received = serializers.ChoiceField(
        choices=_choices(CheckOut.YES_NO_CHOICES), required=False, allow_null=True
    )
    key_return_date = serializers.DateField(required=False, allow_null=True)
    key_return_status = serializers.ChoiceField(
        choices=_choices(CheckOut.KEY_RETURN_STATUS_CHOICES), required=False, allow_null=True
    )

    def create(self, validated_data) -> CheckOutKeyReturnUpdateRequest:
        return CheckOutKeyReturnUpdateRequest(**validated_data)


class CheckOutCommentsUpdateSerializer(serializers.Serializer):
    check_out_id = serializers.IntegerField()
    internal_comments = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tenant_remarks = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    special_instructions = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def create(self, validated_data) -> CheckOutCommentsUpdateRequest:
        return CheckOutCommentsUpdateRequest(**validated_data)


class CheckOutDocumentsUpdateSerializer(serializers.Serializer):
    check_out_id = serializers.IntegerField()
    documents_notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def create(self, validated_data) -> CheckOutDocumentsUpdateRequest:
        return CheckOutDocumentsUpdateRequest(**validated_data)
