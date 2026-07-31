from rest_framework import serializers
from pms_apps.property.dataclasses.requests.property_assignment_update import PropertyAssignmentUpdateRequest


class PropertyAssignmentUpdateSerializer(serializers.Serializer):
    property_assignment_id = serializers.IntegerField()
    assignment_status = serializers.ChoiceField(
        choices=["Pending", "Approved", "Active", "Completed", "Cancelled"],
        required=False, allow_null=True
    )
    tenant_type = serializers.ChoiceField(
        choices=["Individual", "Corporate"],
        required=False, allow_null=True
    )
    company_name = serializers.CharField(max_length=255, required=False, allow_null=True)
    rental_start_date = serializers.DateField(required=False, allow_null=True)
    rental_end_date = serializers.DateField(required=False, allow_null=True)
    agreement_duration_months = serializers.IntegerField(required=False, allow_null=True)
    maintenance_charges = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False, allow_null=True
    )
    advance_rent_paid = serializers.BooleanField(required=False, allow_null=True)
    payment_mode = serializers.ChoiceField(
        choices=["Cash", "Bank Transfer", "Online", "Cheque"],
        required=False, allow_null=True
    )
    agreement_type = serializers.ChoiceField(
        choices=["Government Agreement", "Internal Agreement"],
        required=False, allow_null=True
    )
    agreement_status = serializers.ChoiceField(
        choices=["Pending", "Prepared", "Signed", "Executed", "Terminated"],
        required=False, allow_null=True
    )
    agreement_prepared_by_id = serializers.IntegerField(required=False, allow_null=True)
    key_available_in_office = serializers.ChoiceField(
        choices=["Yes", "No"],
        required=False, allow_null=True
    )
    key_code = serializers.CharField(max_length=100, required=False, allow_null=True)
    key_handover_date = serializers.DateField(required=False, allow_null=True)
    key_handover_status = serializers.ChoiceField(
        choices=["Pending", "Handed Over", "Returned"],
        required=False, allow_null=True
    )
    electricity_meter_number = serializers.CharField(max_length=100, required=False, allow_null=True)
    electricity_meter_reading_start = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False, allow_null=True
    )
    water_meter_reading_start = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False, allow_null=True
    )
    gas_meter_reading_start = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False, allow_null=True
    )
    finance_approval_status = serializers.ChoiceField(
        choices=["Pending", "Approved", "On Hold", "Rejected"],
        required=False, allow_null=True
    )
    rent_entry_created = serializers.ChoiceField(
        choices=["No", "Yes"],
        required=False, allow_null=True
    )
    invoice_generated = serializers.ChoiceField(
        choices=["No", "Yes"],
        required=False, allow_null=True
    )
    maintenance_required = serializers.ChoiceField(
        choices=["No", "Yes"],
        required=False, allow_null=True
    )
    maintenance_ticket_id = serializers.CharField(max_length=100, required=False, allow_null=True)
    maintenance_status = serializers.ChoiceField(
        choices=["Pending", "In Progress", "Completed", "Not Required"],
        required=False, allow_null=True
    )
    internal_notes = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tenant_special_requirements = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data) -> PropertyAssignmentUpdateRequest:
        return PropertyAssignmentUpdateRequest(**validated_data)
